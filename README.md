# Twitter Otomasyon Merkezi (Terminal CLI)

Bu proje, terminal üzerinden yönetilebilen, **Ungoogled Chromium** ve **Playwright** tabanlı tam otomatik bir Twitter bot ve betik enjeksiyon sistemidir. 

Temel amacı, her biri izole edilmiş farklı tarayıcı profillerinde (farklı hesaplarla) paralel işlemler yürütebilmek ve özel olarak yazılmış tarayıcı eklentisi sayesinde bu oturumları sonlandırmadan dinamik olarak JavaScript betiklerini sayfalarda çalıştırabilmektir.

## 🚀 Öne Çıkan Özellikler

- **Tam Otomatik Hesap Yönetimi:** SQLite veritabanı ile çoklu Twitter hesabının müsaitlik durumunu takip eder ve oturum başlatır.
- **Ungoogled Chromium Desteği:** Özellikle gizlilik, hız ve parmak izi koruması (anti-fingerprinting) için Google servislerinden arındırılmış Chromium sürümünü kullanır. Uygulama özel Chromium flag'leri ile başlatılır.
- **Dinamik Betik Enjeksiyonu:** Sistemle entegre çalışan yerel tarayıcı eklentisi (extension), arkaplanda çalışan FastAPI sunucusuna belirli aralıklarla ping atarak verilen yeni JS betiklerini anında algılar ve açık olan Twitter sekmelerine enjekte eder. Oturumları yeniden başlatmadan kodu güncelleyebilirsiniz.
- **CLI (Terminal) Arayüzü:** Tüm bu işlemler sade, karmaşadan uzak ve menü tabanlı bir terminal arayüzünden (`app.py`) kontrol edilir.
- **Memory-Bank:** Projenin son durumunu ve mimarisini takip etmeyi sağlayan bir bellek yapısına sahiptir.

## ⚙️ Kurulum ve Kullanım

### Gereksinimler
- Python 3.10 veya üzeri
- [Ungoogled Chromium](https://github.com/ungoogled-software/ungoogled-chromium) (.exe yolu yapılandırılmalıdır)

### Adımlar

1. Depoyu klonlayın:
```bash
git clone https://github.com/KULLANICI_ADINIZ/twitter_back.git
cd twitter_back
```

2. Gerekli kütüphaneleri yükleyin ve Playwright'ı hazırlayın:
```bash
pip install -r requirements.txt
playwright install
```

3. `config.json` dosyasını açıp Ungoogled Chromium'un bilgisayarınızdaki yolunu (`chromium_path`) düzenleyin. 

4. Uygulamayı başlatın:
```bash
python app.py
```

Menü üzerinden hesap ekleyebilir, oturum başlatabilir ve dinamik olarak çalışacak yeni JavaScript kodunuzun yolunu terminalden belirterek anlık olarak güncelleyebilirsiniz.
