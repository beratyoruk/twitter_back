# Twitter Otomasyon - Çoklu Oturum Yöneticisi (v2.0.0)

Bu proje, **Ungoogled Chromium** kullanarak birden fazla Google ve Twitter hesabını kalıcı profillerle, bot tespitine takılmadan (Playwright veya Selenium CDP kullanmadan) yönetmenizi sağlayan bir terminal uygulamasıdır.

## 🚀 Öne Çıkan Özellikler

- **Sıfır Bot Tespiti:** Google giriş otomasyonu, tarayıcı arka kapı protokolleri (CDP) üzerinden yapılmaz. Tarayıcı ön plana alınarak işletim sistemi düzeyinde fiziksel klavye/fare simülasyonu (`pynput`, `pyautogui`) ile gerçek bir insan gibi giriş yapılır.
- **Kalıcı (Persistent) Çerezler:** Oturumu kapattığınızda veya durdurduğunuzda, arka planda tarayıcı nazikçe (`graceful shutdown`) kapatılır. Böylece Google ve Twitter çerezleriniz (`cookies`) diske şifrelenmiş halde başarıyla yazılır. Bir sonraki açılışta tekrar şifre girmenize gerek kalmaz.
- **Çoklu Sekme (Multi-tab) Başlatma:** Kayıtlı bir oturumu açtığınızda hem `My Account (Google)` hem de `Twitter` sekmeleri eşzamanlı olarak açılır.
- **Güvenli Veritabanı:** Oturum durumlarınız (Açık/Kapalı), süreç ID'leri (PID) `SQLite` veritabanında (`sessions.db`) güvenle tutulur.
- **Arka Plan Monitörü:** Arka planda çalışan bir thread sayesinde, elinizle tarayıcıyı kapattığınızda bile program 10 saniye içinde bunu fark edip veritabanındaki durumu "🔴 Kapalı" olarak günceller.
- **Temiz Profil Yönetimi:** Oturumu sildiğinizde hedefe ait tüm alt süreçler (Chrome Renderer, GPU, Extension Helper) temizlenir ve diskteki profil klasörü güvenli bir döngü ile tamamen kazınır.

## 🛠 Mimari (v2.0.0)

Eski `Playwright` bağımlılıkları tamamen kaldırılmış, süreç (`subprocess`) mimarisi doğrudan Chromium executable'ı üzerinden yapılandırılmıştır. 
Tüm veriler cihazınızda `profiles/` klasörü altında izole olarak tutulur.

## 📋 Gereksinimler

- Python 3.10 veya üzeri
- Windows İşletim Sistemi
- [Ungoogled Chromium (Portapps)](https://portapps.io/app/ungoogled-chromium-portable/) yüklü olmalıdır.

## ⚙️ Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/beratyoruk/twitter_back.git
   cd twitter_back
   ```

2. Gereksinimleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. `config.json` dosyanızı oluşturun ve Chromium yolunuzu ayarlayın:
   ```json
   {
       "chromium_path": "C:/portapps/ungoogled-chromium-portable/app/chrome.exe",
       "extension_path": "extension"
   }
   ```

## 🎮 Kullanım

Terminale aşağıdaki komutu yazarak menüye erişebilirsiniz:

```bash
python main.py
```

### Menü Seçenekleri:
1. **Yeni Oturum Ekle:** E-posta ve şifrenizi terminale girersiniz. Tarayıcı açılır, otomatik olarak insan gibi giriş yapar ve profilinizi kaydeder.
2. **Oturumları Listele:** Kayıtlı tüm hesaplarınızı ve o anki durumlarını (🟢 Aktif / 🔴 Kapalı) listeler.
3. **Açık Oturumu Durdur / Kapat:** Aktif olan bir tarayıcıyı, profili bozmadan nazikçe kapatır. Verileriniz korunur.
4. **Oturum Sil:** Bir hesabı; tarayıcı alt süreçlerinden, SQLite veritabanından ve diskteki profil klasöründen kalıcı olarak siler.
5. **Kayıtlı Oturumları Aç:** Önceden giriş yapılmış ve kapatılmış bir oturumu **şifre girmeden**, direkt Twitter'da olacak şekilde tekrar açmanızı sağlar. Aynı anda 0'a basarak kaydedilmiş tüm oturumlarınızı eşzamanlı başlatabilirsiniz.
