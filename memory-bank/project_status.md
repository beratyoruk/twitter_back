# Proje Durumu (Project Status)

## Temel Hedefler
- [x] Terminal üzerinden yönetilebilen (CLI) tam otomatik bir sistem kurmak.
- [x] Ungoogled Chromium kullanarak Twitter otomasyonu için tarayıcı oturumları yönetmek.
- [x] Terminal'de `1` tuşuna basılınca: Yeni tarayıcı oturumu açma, müsait bir Twitter hesabıyla giriş yapma, eklentiyi yükleme ve betiği çalıştırma.
- [x] Terminal'de `2` tuşuna basılınca: Seçilen açık oturumları kapatma ve hesabın durumunu "müsait" olarak güncelleme.
- [x] Terminal'de `3` tuşuna basılınca: Oturumu sonlandırmadan, eklenti içindeki betiği dışarıdan verilen yeni betik ile güncelleme.
- [x] Ungoogled Chromium flag'lerini dokümantasyona (flags.md) göre entegre etme.
- [x] Tüm işlemleri Github'a düzgün açıklamalarla pushlama.
- [x] Minimum yorum satırı ile python backend'ini yazma.

## Yapılacaklar (TODO)
- Kullanıcının "Ungoogled Chromium" exe yolunu `config.json`'da güncellemesi.

## Tamamlananlar
- Code Github'a başarıyla PUSHlandı! (https://github.com/beratyoruk/twitter_back)
- Memory-bank oluşturuldu.
- `app.py`, `worker.py`, `server.py` ve DB yönetimi için `account_manager.py` kodlandı.
- Local ağ üzerinde `127.0.0.1:9090/script.js` hizmeti sunan FastAPI sunucusu aktif.
- Local sunucuya belirli saniyelerle ping atıp yeni JS'i evaluate eden bir "betik çalıştırıcı eklenti" altyapısı kuruldu.
