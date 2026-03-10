# Bilinen Sorunlar (Known Issues)

## #1 — Google: "Bu tarayıcı veya uygulama güvenli görünmüyor"

### Açıklama
Playwright ile kontrol edilen tarayıcılarda `navigator.webdriver` özelliği varsayılan olarak `true` döner. Google bu değeri tespit edip otomasyonla açılmış tarayıcıları güvensiz sayarak girişi bloklar.

### Geçici Çözüm (Uygulandı)
`--disable-blink-features=AutomationControlled` Chromium flag'i ve aşağıdaki `init_script` eklendi:
```js
Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
```
Bu, temel bot tespitini büyük ölçüde azaltır. Ancak bazı Google hesaplarında hâlâ tetiklenebilir.

### Kalıcı Çözüm Önerileri
1. **Manuel Profil Hazırlama:** Ungoogled Chromium'u normalde açıp Google'a manuel giriş yapıp kapatın. Oluşan profil `profiles/` klasörüne kopyalanırsa sonraki script çalışmalarında hesap zaten giriş yapmış olacak, Google giriş ekranını görmeyecek.
2. **App Password Kullanımı:** Google hesabında 2 Adımlı Doğrulama açıksa Gmail Uygulama Şifresi (`myaccount.google.com/apppasswords`) oluşturup normal şifre yerine onu kullanın.
3. **Playwright-Stealth:** `playwright-stealth` veya `undetected-playwright` kütüphaneleri daha gelişmiş bot maskeleme sağlar (araştırma aşamasında).

### Durum
- [ ] Araştırılıyor
