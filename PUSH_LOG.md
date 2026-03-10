# Push Log

## [v1.3.0] - 2026-03-11
**Çoklu Oturum Yönetimi**
- `main.py` 4 seçenekli interaktif CLI menüsüne dönüştürüldü.
- `worker.py` login/resume modlarını destekler hale getirildi.
- `sessions.json` ile kalıcı oturum kaydı eklendi.
- Google opsiyonel adımları (ev adresi, telefon, gizlilik) otomatik atlanıyor.
- Oturum resume'da profil çerezleri kullanılır, yeniden giriş yapılmaz.
- `v1.3-multi-session` branch'i oluşturuldu.

## [v1.2.0] - 2026-03-11
**Proje Sadeleştirme + Kullanıcı Kurulum Rehberi**
- Proje tek bir işe (`main.py`) indirgendi; tüm gereksiz dosyalar silindi.
- `README.md` baştan yazıldı: kurulum adımları, yapılandırma ve kullanım.
- `ISSUES.md` oluşturuldu: bilinen sorunlar ve çözüm önerileri belgelendi.
- `browser.wait_for_event` çöküşü düzeltildi; yerine sayfa döngüsü (loop) kullanıldı.
- `--disable-blink-features=AutomationControlled` ve `navigator.webdriver` gizleme eklendi.

## [v1.1.0] - 2026-03-10
**Google Giriş Otomasyonu + 2FA Desteği**
- Google Accounts sayfasına insan gibi yazarak otomatik giriş.
- 2FA / SMS gelirse tarayıcı bekler, kullanıcı manuel tamamlar.
- Ungoogled Chromium flag listesi tamamen entegre edildi.

## [v1.0.0] - 2026-03-10
**İlk Yükleme**
- Temel proje iskeleti: CLI menüsü, çoklu hesap yönetimi, FastAPI betik sunucusu.
- SQLite ile hesap/oturum veritabanı.
- Chrome eklentisi: local API'dan betik çekip Twitter sayfalarına enjekte eder.
