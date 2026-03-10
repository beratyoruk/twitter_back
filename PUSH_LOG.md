# Push Log (Versiyon ve Değişiklik Kayıtları)

Bu dosya, Github'a yapılan her yüklemede (push) nelerin değiştiğini, güncellendiğini ve eklendiğini kayıt altında tutmak için oluşturulmuştur.

## [v1.0.0] - 2026-03-10
**İlk Yükleme (Initial Commit)**

### Eklenenler:
- Projenin temel iskeleti oluşturuldu.
- Terminal / CLI menüsü olarak hizmet verecek olan `app.py` yazıldı. 
- Tarayıcıyı Ungoogled Chromium ayarlarına (flags) göre başlatan `worker.py` eklendi.
- Paralel tarayıcı işlemlerini yöneten `browser_manager.py` oluşturuldu.
- Hesapların müsait/meşgul durumlarını yerel SQLite veritabanında tutan `account_manager.py` kodlandı.
- Eklentinin anlık betik dosyalarını okuyabilmesi için FastAPI tabanlı `server.py` aktif edildi.
- Twitter sekmelerine dinamik olarak betikleri enjekte edecek olan tarayıcı eklentisi (`extension/` klasörü) kodlandı.
- `memory-bank` klasörü ve proje mimari durum dosyaları, ayrıca bağımlılıkları içeren `requirements.txt` ve `config.json` eklendi.
