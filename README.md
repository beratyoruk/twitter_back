# Twitter Otomasyon - Ungoogled Chromium ile Çoklu Oturum Yönetimi

Ungoogled Chromium üzerinde izole, kalıcı tarayıcı profilleriyle birden fazla Google/Twitter hesabını aynı anda yöneten Python aracı.

## Özellikler
- **Çoklu Oturum:** Her hesap ayrı bir Chromium penceresinde, ayrı profille açılır.
- **Kalıcı Profil:** `profiles/` klasöründe kayıtlı oturumlar; yeniden açıldığında Google/Twitter girişi tekrar yapılmaz.
- **Human-like Yazma:** Bot tespitini azaltmak için karakterler arasında gecikme.
- **`playwright-stealth`:** Google'ın otomasyon sinyallerini otomatik maskeler.
- **Google Opsiyonel Adım Atlama:** Ev adresi, telefon, gizlilik ekranları otomatik atlanır.
- **Ungoogled Chromium Flags:** Parmak izi maskeleme, referrer kaldırma, WebRTC kısıtlama dahil tüm gizlilik parametreleri.

## Gereksinimler
- Python 3.10+
- [Ungoogled Chromium / Portapps](https://portapps.io/app/ungoogled-chromium-portable/)

## Kurulum

```bash
git clone https://github.com/beratyoruk/twitter_back.git
cd twitter_back
pip install -r requirements.txt
python -m playwright install
```

## Yapılandırma
`config.json` içindeki `chromium_path` değerini Ungoogled Chromium `chrome.exe` yoluyla güncelleyin:

```json
{
    "chromium_path": "C:/portapps/ungoogled-chromium-portable/app/chrome.exe",
    "extension_path": "extension"
}
```

## Kullanım

```bash
python main.py
```

| Seçenek | Açıklama |
|---------|----------|
| **1** | Yeni oturum ekle — mail/şifre gir, Google'a giriş yap, Twitter aç |
| **2** | Aktif/kayıtlı oturumları listele |
| **3** | Oturum sil (profil dahil opsiyonel) |
| **4** | Kayıtlı oturumları yeniden aç (çerezlerle, giriş gerekmez) |

## Proje Yapısı

```
twitter_back/
├── main.py          # CLI menüsü
├── worker.py        # Playwright tarayıcı süreç yönetimi
├── config.json      # Chromium ve eklenti yolu
├── requirements.txt
├── extension/       # Tarayıcı eklentisi
├── profiles/        # Hesap profilleri (git'e eklenmez)
├── sessions.json    # Oturum kayıtları (git'e eklenmez)
├── ISSUES.md        # Bilinen sorunlar
└── PUSH_LOG.md      # Versiyon geçmişi
```

## Bilinen Sorunlar
Bkz. [ISSUES.md](./ISSUES.md)
