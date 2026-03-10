import sys
import json
import os
import time
from playwright.sync_api import sync_playwright

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Varsayılan yapılandırma
        return {
            "chromium_path": "", # Kullanıcı ungoogled chromium yolunu belirtmeli
            "extension_path": "my_extension" # Uzantının dizini
        }

def start_worker(account_id, username, password, profile_dir):
    config = load_config()
    chrome_path = config.get("chromium_path")
    extension_path = os.path.abspath(config.get("extension_path", "my_extension"))
    
    # Eklenti klasörü yoksa boş bir tane oluştur(hata almamak için)
    if not os.path.exists(extension_path):
        os.makedirs(extension_path, exist_ok=True)
        # Basit bir manifest yaz ki chromium kabul etsin
        with open(os.path.join(extension_path, "manifest.json"), "w") as f:
            f.write('{"manifest_version": 3, "name": "Betiği Çalıştırıcı", "version": "1.0"}')
    
    with sync_playwright() as p:
        args = [
            # Ungoogled Chromium Flags (Dokümantasyondan birkaç pratik örnek):
            "--disable-search-engine-collection",
            "--fingerprinting-canvas-image-data-noise",
            "--fingerprinting-client-rects-noise",
            "--popups-to-tabs",
            # Eklenti Yükleme Flags
            f"--disable-extensions-except={extension_path}",
            f"--load-extension={extension_path}"
        ]

        kwargs = {
            "user_data_dir": profile_dir,
            "headless": False,
            "args": args
        }
        
        if chrome_path and os.path.exists(chrome_path):
            kwargs["executable_path"] = chrome_path
        
        try:
            browser = p.chromium.launch_persistent_context(**kwargs)
        except Exception as e:
            print(f"Tarayıcı başlatılırken hata: {e}")
            return
            
        # Yeni bir sekme aç ve Twitter'a git
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://twitter.com/login")
        
        # Eğer henüz giriş yapılmamışsa (cookie yoksa) UI üzerinden otomatik login olabiliriz.
        # Basit bir Twitter Login otomasyonu bloğu:
        try:
            # Bekleme limitleriyle login fieldlarını ara.
            page.wait_for_selector('input[autocomplete="username"]', timeout=5000)
            page.fill('input[autocomplete="username"]', username)
            page.keyboard.press('Enter')
            
            page.wait_for_selector('input[name="password"]', timeout=5000)
            page.fill('input[name="password"]', password)
            page.keyboard.press('Enter')
            
            print(f"[{username}] için Worker giriş denemesini tamamladı.")
        except Exception as e:
            # Muhtemelen zaten login olunmuştur ( persistent profile ) veya ağ hatası
            pass
            
        # Betiğin güncellenmesi ile tarayıcıdaki betik nasıl iletişim kuracak?
        # En basit yol: Python betiği (bu worker.py) her X saniyede bir lokaldeki 'current_script.js' yi eval edebilir,
        # Ya da eklentin kendi içinde bir polling(ör: local server'dan GET isteği) yapar.
        
        print(f"[{username}] Worker çalışıyor. Çıkmak için işlemi sonlandırın.")
        # Sürecin kapanmaması için sonsuz döngü:
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            browser.close()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Kullanım: python worker.py <account_id> <username> <password> <profile_dir>")
        sys.exit(1)
        
    acc_id = sys.argv[1]
    usr = sys.argv[2]
    pwd = sys.argv[3]
    p_dir = sys.argv[4]
    
    start_worker(acc_id, usr, pwd, p_dir)
