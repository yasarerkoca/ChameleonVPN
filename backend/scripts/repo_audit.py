#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
repo_audit.py
- Depo dizin yapısını yazdırır (ağaç görünümü)
- Gereksiz klasörleri yok sayar
- app.* importlarının dosya sisteminde gerçekten var olup olmadığını statik olarak (AST ile) kontrol eder
- Çift (aynı ada sahip) Python dosyalarını raporlar
Not: Sadece KONTROL yapar; dosya/şema değiştirmez.
"""

import os
import sys
import argparse
import ast
from typing import Iterable, List, Tuple, Dict, Set

IGNORED_DIRS = {
    ".git", ".github", ".venv", "venv", "__pycache__", "node_modules",
    "dist", "build", ".mypy_cache", ".pytest_cache", "logs"
}

def is_ignored(name: str) -> bool:
    return name in IGNORED_DIRS or name.startswith(".")

def list_dir(path: str) -> Tuple[List[str], List[str]]:
    """return (dirs, files) sorted"""
    try:
        items = os.listdir(path)
    except OSError:
        return [], []
    dirs, files = [], []
    for it in items:
        if is_ignored(it):
            continue
        full = os.path.join(path, it)
        if os.path.isdir(full):
            dirs.append(it)
        else:
            files.append(it)
    return sorted(dirs), sorted(files)

def print_tree(root: str, max_depth: int, show_files: bool = True, prefix: str = "") -> None:
    if max_depth < 0:
        return
    dirs, files = list_dir(root)
    entries: List[Tuple[str, bool]] = [(d, True) for d in dirs]
    if show_files:
        entries += [(f, False) for f in files]

    for idx, (name, is_dir) in enumerate(entries):
        is_last = (idx == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        print(prefix + connector + name)
        if is_dir and max_depth > 0:
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(os.path.join(root, name), max_depth - 1, show_files, new_prefix)

def dotpath_exists(pkg_root: str, dotpath: str) -> bool:
    """
    app.models.user -> /app/app/models/user.py  veya  /app/app/models/user/__init__.py
    """
    parts = dotpath.split(".")
    base = os.path.join(pkg_root, *parts)
    py_file = base + ".py"
    pkg_init = os.path.join(base, "__init__.py")
    return os.path.isfile(py_file) or os.path.isfile(pkg_init)

def collect_python_files(root: str, within: str = "app") -> List[str]:
    result: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # ignore
        dirnames[:] = [d for d in dirnames if not is_ignored(d)]
        for fn in filenames:
            if fn.endswith(".py") and not fn.startswith("."):
                full = os.path.join(dirpath, fn)
                # yalnızca /app/app altında (within) bakmak istiyoruz
                rel = os.path.relpath(full, root)
                if rel.split(os.sep)[0] == within:
                    result.append(full)
    return result

def resolve_imports_in_file(pyfile: str) -> Set[str]:
    """
    app.* importlarını çıkartır (from app.x.y import z  / import app.x.y)
    """
    src = ""
    try:
        with open(pyfile, "r", encoding="utf-8") as f:
            src = f.read()
    except Exception:
        return set()

    try:
        tree = ast.parse(src, filename=pyfile)
    except SyntaxError:
        # Syntax hatalı dosya varsa sadece atla, raporlamayı bozmasın
        return set()

    wanted: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name  # "app.x.y" olabilir
                if name == "app" or name.startswith("app."):
                    wanted.add(name)
        elif isinstance(node, ast.ImportFrom):
            # from app.x.y import Z
            if node.module and (node.module == "app" or node.module.startswith("app.")):
                wanted.add(node.module)
    return wanted

def audit_imports(pkg_root: str) -> Tuple[List[str], List[str]]:
    """
    Dönüş:
      - errors: bulunamayan app.* modülleri
      - checked: kontrol edilen dosya listesi (bilgi amaçlı)
    """
    pyfiles = collect_python_files(pkg_root, within="app")
    missing: Set[str] = set()
    for f in pyfiles:
        imps = resolve_imports_in_file(f)
        for mod in imps:
            if not dotpath_exists(pkg_root, mod):
                missing.add(mod)
    return sorted(missing), pyfiles

def duplicate_basenames(pyfiles: List[str]) -> Dict[str, List[str]]:
    """
    Aynı adda (basename) birden fazla .py dosyası var mı?
    Örn: user.py birden fazla dizinde—bu kötü olmak zorunda değil ama potansiyel kafa karıştırır.
    """
    table: Dict[str, List[str]] = {}
    for f in pyfiles:
        base = os.path.basename(f)
        table.setdefault(base, []).append(f)
    return {k: v for k, v in table.items() if len(v) > 1}

def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Depo denetimi (salt-kontrol).")
    ap.add_argument("--pkg-root", default="/app", help="Container içindeki proje kökü (default: /app)")
    ap.add_argument("--max-depth", type=int, default=4, help="Ağaç yazdırma derinliği (default: 4)")
    ap.add_argument("--no-files", action="store_true", help="Sadece klasörleri göster")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.pkg_root)
    if not os.path.isdir(root):
        print(f"ERROR: Klasör yok: {root}", file=sys.stderr)
        return 2

    print(f"== TREE: {root} ==")
    print_tree(root, max_depth=args.max_depth, show_files=not args.no_files)
    print()

    print("== IMPORT AUDIT: app.* ==")
    missing, checked_files = audit_imports(root)
    if missing:
        print("Bulunamayan modül(ler):")
        for m in missing:
            print("  -", m)
    else:
        print("app.* importları dosya sisteminde çözümlenebiliyor (OK)")
    print()

    print("== DUPLICATE BASENAMES ==")
    dups = duplicate_basenames(checked_files)
    if dups:
        for base, paths in dups.items():
            print(f"  {base}:")
            for p in paths:
                print("    -", p)
    else:
        print("Aynı ada sahip birden fazla .py dosyası yok (OK)")

    # exit code politikasını yumuşak tutalım:
    # - eksik import varsa 1
    # - diğer uyarılar 0
    return 1 if missing else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
