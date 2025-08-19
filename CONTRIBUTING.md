# Katkı Rehberi

Projeye katkı yapmak için:
1. Fork edip kendi dalınızda geliştirme yapın.
2. Testleri geçirdiğinizden emin olun.
3. Linter kurallarına uyun.
4. Pull Request açarken detaylı açıklama ekleyin.
5. Yeni paket eklerken `backend/requirements.in` ve `requirements.txt` dosyalarını `pip-compile` ile güncelleyin.
6. Bağımlılıklarda güvenlik açıklarını taramak için `pip-audit` çalıştırın.
Dizinler:
- backend: Python (API)
- mobile: Flutter (mobil)
- frontend/web-admin, frontend/web-user: React (web)
- tests: Ek testler

Sorular için issues kısmını kullanabilirsiniz.
