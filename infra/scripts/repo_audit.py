#!/usr/bin/env python3
# scripts/repo_audit.py

import os
import sys
import ast
import argparse
from pathlib import Path
from collections import defaultdict

IGNORES = {
    ".git", ".idea", ".vscode", "__pycache__", ".mypy_cache", ".pytest_cache",
    "node_modules", "dist", "build", ".venv", "venv", ".tox"
}

def is_pkg_dir(p: Path) -> bool:
    return (p / "__init__.py").exists()

def walk_tree(root: Path, max_depth: int, only_py: bool):
    """Yield (path, depth, is_dir) for tree printing."""
    root = root.resolve()
    def _walk(base: Path, depth: int):
        if depth > max_depth:
            return
        try:
            items = sorted([p for p in base.iterdir()], key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            return
        for p in items:
            if p.name in IGNORES:
                continue
            if p.is_dir():
                yield p, depth, True
                _walk(p, depth + 1)
            else:
                if only_py and p.suffix != ".py":
                    continue
                yield p, depth, False
    yield root, 0, True
    yield from _walk(root, 1)

def print_tree(root: Path, max_depth: int, only_py: bool):
    """Pretty tree output."""
    # Basit bir tree – çizgi karakterleri olmadan, derinlik ile girinti
    for p, depth, is_dir in walk_tree(root, max_depth, only_py):
        rel = p.relative_to(root)
        prefix = "  " * (depth - 1) if depth > 0 else ""
        tag = "/" if is_dir else ""
        print(f"{prefix}{rel}{tag}")

def find_missing_inits(pkg_root: Path):
    """__init__.py eksik olan (içinde .py bulunan) klasörleri bul."""
    missing = []
    for base, dirs, files in os.walk(pkg_root):
        base_p = Path(base)
        if base_p.name in IGNORES or any(part in IGNORES for part in base_p.parts):
            continue
        py_files = [f for f in files if f.endswith(".py")]
        if py_files:
            if not (base_p / "__init__.py").exists():
                missing.append(base_p)
    return missing

def module_path_exists(pkg_root: Path, module: str) -> bool:
    """
    'app.models.user.user_notification' gibi bir modülü dosya sisteminde arar.
    pkg_root altında 'app' klasörü bulundu varsayımıyla çalışır.
    """
    if not module or not module.startswith("app"):
        return True  # sadece app.* modüllerini sıkı kontrol ediyoruz
    base = pkg_root / module.replace(".", "/")
    # modül bir dosya olabilir
    if (base.with_suffix(".py")).exists():
        return True
    # veya paket olabilir
    if (base / "__init__.py").exists():
        return True
    return False

def infer_imported_modules_from_file(pyfile: Path):
    """AST ile import edilen 'app.*' modüllerini çıkar."""
    mods = set()
    try:
        src = pyfile.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return mods
    try:
        tree = ast.parse(src, filename=str(pyfile))
    except SyntaxError:
        # Syntax hatalı dosyayı raporlamak istemiyoruz; sadece es geçelim
        return mods

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                name = n.name
                if name.startswith("app."):
                    mods.add(name)
                elif name == "app":
                    mods.add("app")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mod = node.module
                # from app.models import user gibi
                if mod.startswith("app"):
                    # alt isimleri modül gibi kontrol etmek daha sağlıklı
                    # ör: from app.models.user import user_notification
                    if node.names:
                        for n in node.names:
                            # alt modül gibi deneyelim
                            candidate = f"{mod}.{n.name}"
                            # Hem candidate’i hem mod’u listeye ekleyelim
                            mods.add(mod)
                            mods.add(candidate)
                    else:
                        mods.add(mod)
    return mods

def check_import_targets(pkg_root: Path):
    """Tüm .py dosyalarını dolaşıp app.* import’larının gerçekten var olup olmadığını kontrol eder."""
    missing = defaultdict(set)  # {pyfile: {module1, module2}}
    for base, dirs, files in os.walk(pkg_root):
        base_p = Path(base)
        if base_p.name in IGNORES or any(part in IGNORES for part in base_p.parts):
            continue
        for f in files:
            if not f.endswith(".py"):
                continue
            pyfile = base_p / f
            mods = infer_imported_modules_from_file(pyfile)
            for m in mods:
                if not module_path_exists(pkg_root, m):
                    missing[str(pyfile)].add(m)
    return missing

def find_duplicate_module_names(pkg_root: Path):
    """
    Aynı ada sahip (stem) ama farklı klasörlerde yer alan .py dosyalarını listeler.
    Bu bazen import gölgelemesine yol açabilir.
    """
    stems = defaultdict(list)
    for base, dirs, files in os.walk(pkg_root):
        base_p = Path(base)
        if base_p.name in IGNORES or any(part in IGNORES for part in base_p.parts):
            continue
        for f in files:
            if f.endswith(".py"):
                stems[Path(f).stem].append(str(base_p / f))
    dups = {stem: paths for stem, paths in stems.items() if len(paths) > 1}
    return dups

def main():
    ap = argparse.ArgumentParser(description="Repo dosya yapısı denetimi")
    ap.add_argument("--pkg-root", default="backend", help="`app/` paketinin bulunduğu kök klasör (host: backend, container: /app)")
    ap.add_argument("--max-depth", type=int, default=4, help="Ağaç yazdırma derinliği")
    ap.add_argument("--only-py", action="store_true", help="Ağaçta sadece .py dosyalarını göster")
    ap.add_argument("--no-tree", action="store_true", help="Ağaç görünümünü yazdırma")
    args = ap.parse_args()

    pkg_root = Path(args.pkg_root).resolve()
    app_dir = pkg_root / "app"
    if not app_dir.exists():
        print(f"[HATA] '{pkg_root}' altında 'app/' bulunamadı. --pkg-root değerini kontrol edin.", file=sys.stderr)
        sys.exit(2)

    print(f"==> Paket kökü: {pkg_root}")
    print(f"==> App dizini: {app_dir}\n")

    # 1) Tree
    if not args.no_tree:
        print("— DOSYA AĞACI —")
        print_tree(pkg_root, args.max_depth, args.only_py)
        print()

    # 2) __init__.py eksikleri
    print("— __init__.py KONTROLÜ —")
    missing = find_missing_inits(app_dir)
    if not missing:
        print("OK: Paket olması gereken klasörlerde __init__.py eksik görünmüyor.\n")
    else:
        for p in missing:
            print(f"[UYARI] __init__.py eksik: {p}")
        print()

    # 3) app.* import hedefleri var mı?
    print("— IMPORT HEDEF KONTROLÜ (app.*) —")
    missing_imports = check_import_targets(pkg_root)
    if not missing_imports:
        print("OK: app.* import’larının hepsi dosya sisteminde karşılık buluyor.\n")
    else:
        for pyfile, mods in missing_imports.items():
            print(f"[UYARI] {pyfile} dosyasında bulunamayan modüller:")
            for m in sorted(mods):
                print(f"   - {m}")
        print()

    # 4) Modül adı çakışmaları
    print("— MODÜL ADI ÇAKIŞMALARI —")
    dups = find_duplicate_module_names(app_dir)
    if not dups:
        print("OK: Aynı ada sahip birden fazla .py dosyası tespit edilmedi.\n")
    else:
        for stem, paths in dups.items():
            print(f"[UYARI] '{stem}.py' birden fazla yerde var:")
            for p in paths:
                print(f"   - {p}")
        print()

    print("Denetim tamamlandı ✅")

if __name__ == "__main__":
    main()
