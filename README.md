# Twitter Otomasyon - Ungoogled Chromium ile Oturum Yönetimi

Ungoogled Chromium üzerinde izole, kalıcı tarayıcı profilleriyle Google (ve ardından Twitter) hesabına otomatik giriş yapan Python tabanlı araç.

## Özellikler
- **Kalıcı Profil:** Her hesap için ayrı `profiles/` klasörü oluşturulur. Bir sonraki açılışta oturum devam eder.
- **İnsan Gibi Yazma:** Giriş alanlarına karakterler arası gecikmeyle yazılır (bot tespitini azaltır).
- **2FA / SMS Desteği:** Google ek doğrulama isterse tarayıcı ekranda durur; siz manuel tamamlarsınız.
- **Ungoogled Chromium Flags:** Parmak izi maskeleme, referrer kaldırma, WebRTC sınırlama gibi tüm gizlilik parametreleri etkin.
- **Eklenti Desteği:** `extension/` klasöründeki Chrome uzantısı otomatik yüklenir.

## Gereksinimler
- Python 3.10+
- [Ungoogled Chromium](https://github.com/ungoogled-software/ungoogled-chromium) (Portapps önerilir)

## Kurulum

```bash
# 1. Depoyu klonlayın
git clone https://github.com/beratyoruk/twitter_back.git
cd twitter_back

# 2. Playwright'i kurun
pip install -r requirements.txt
python -m playwright install
```

## Yapılandırma
`config.json` dosyasını açıp `chromium_path` değerini kendi Ungoogled Chromium `chrome.exe` dosyanızın yolu ile güncelleyin:

```json
{
    "chromium_path": "C:/portapps/ungoogled-chromium-portable/app/chrome.exe",
    "extension_path": "extension"
}
```

**Windows için Ungoogled Chromium nasıl kurulur?**
1. [Portapps - Ungoogled Chromium](https://portapps.io/app/ungoogled-chromium-portable/) adresinden indirin.
2. Kurulum sonrası oluşan `chrome.exe` dosyasının tam yolunu `config.json`'a yazın.

## Kullanım

```bash
python main.py
```

Program mail adresinizi ve şifrenizi soracak, ardından tarayıcıyı açacak ve giriş işlemini otomatik gerçekleştirecektir. Google ek doğrulama (2FA, SMS, telefon onayı) isterse tarayıcıda manuel olarak tamamlanabilir.

## Bilinen Sorunlar

Bkz. [ISSUES.md](./ISSUES.md)

## Proje Yapısı
```
twitter_back/
├── main.py          # Ana çalıştırıcı
├── config.json      # Chromium ve eklenti yolu
├── requirements.txt # Python bağımlılıkları
├── extension/       # Tarayıcı eklentisi
├── profiles/        # Hesap profilleri (git'e eklenmez)
└── ISSUES.md        # Bilinen sorunlar ve çözümler
```
