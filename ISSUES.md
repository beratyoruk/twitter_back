# Bilinen Sorunlar (Known Issues)

## #1 — Google: "Bu tarayıcı veya uygulama güvenli görünmüyor"

### Açıklama
Playwright ile kontrol edilen Chromium tarayıcısında `navigator.webdriver` özelliği `true` döner. Google bu sinyali algılayarak otomasyonla açılmış tarayıcılara güvensiz uyarısı gösterir ve girişi bloklar.

### Durum: ✅ Çözüldü

`playwright-stealth` kütüphanesi entegre edildi. `stealth_sync(page)` çağrısı, Google'ın kullandığı tüm otomasyon sinyallerini (webdriver flag, navigator property'leri, Chrome runtime objeleri vb.) otomatik maskeler. Manuel müdahale gerektirmez.

### Uygulanan Çözüm
```python
from playwright_stealth import stealth_sync
stealth_sync(page)  # browser.new_page() sonrası çağrılır
```

### Gereksinim
```
playwright-stealth==2.0.2
```
