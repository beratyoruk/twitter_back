# Mimari (Architecture)

## Sistem Bileşenleri
1. **CLI Arayüzü (app.py)**: Terminal üzerinden kullanıcıdan alınan komutları (1, 2, 3) işler ve ilgili servisleri çağırır.
2. **Hesap Yöneticisi (account_manager.py)**: Müsait olan hesapları getirir, durumu günceller (meşgul/müsait), veritabanı (JSON/SQLite) işlemlerini yönetir.
3. **Tarayıcı Yöneticisi (browser_manager.py)**: Ungoogled Chromium örneklerini başlatır, oturum (profil) yönetimi yapar, eklentiyi yükler ve kapatır. Chromium başlatılırken dokümantasyondaki özel flag'ler (örn. fingerprinting koruması veya performans artırıcı flagler) kullanılır.
4. **Betik/Eklenti Yöneticisi (extension_manager.py)**: Eklentinin içindeki çalışan betiği günceller. Tarayıcı kapanmadan dinamik bir şekilde betik enjeksiyonu veya yerel dosya üzerinden güncelleme yöntemleri kullanılır.

## Veri Modeli
- **Account**:
  - `id`: Benzersiz kimlik
  - `username`: Twitter kullanıcı adı
  - `password`: Twitter şifresi
  - `status`: `available` (müsait) | `in_use` (kullanımda)
  - `profile_dir`: Chromium profil dizini yolu

- **Session**:
  - `session_id`: Oturum kimliği
  - `account_id`: Kullanılan hesabın ID'si
  - `browser_pid`: Çalışan tarayıcı süreci ID'si

## Bağımlılıklar (Tech Stack)
- Python 3.10+
- Playwright (veya Selenium)
- Oturum verileri için SQLite / JSON
