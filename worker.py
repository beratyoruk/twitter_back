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
        return {
            "chromium_path": "",
            "extension_path": "extension"
        }

def start_worker(account_id, username, password, profile_dir):
    config = load_config()
    chrome_path = config.get("chromium_path")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))
    
    if not os.path.exists(extension_path):
        os.makedirs(extension_path, exist_ok=True)
        with open(os.path.join(extension_path, "manifest.json"), "w") as f:
            f.write('{"manifest_version": 3, "name": "Betiği Çalıştırıcı", "version": "1.0"}')
    
    with sync_playwright() as p:
        args = [
            # Ungoogled Chromium Flags (All Platforms)
            "--disable-beforeunload",
            "--disable-search-engine-collection",
            "--fingerprinting-canvas-image-data-noise",
            "--fingerprinting-canvas-measuretext-noise",
            "--fingerprinting-client-rects-noise",
            "--hide-crashed-bubble",
            "--keep-old-history",
            "--max-connections-per-host=15",
            "--popups-to-tabs",
            
            # Windows Specific Portable Data Flags
            "--disable-encryption",
            "--disable-machine-id",
            
            # Desktop Specific 
            "--disable-sharing-hub",
            "--remove-tabsearch-button",
            
            # Existing Chromium Flags
            "--disable-top-sites",
            "--no-default-browser-check",
            "--no-pings",
            "--webrtc-ip-handling-policy=default_public_interface_only",
            
            # Feature Flags
            "--enable-features=MinimalReferrers,NoCrossOriginReferrers,ReducedSystemInfo,RemoveClientHints,SpoofWebGLInfo",
            
            # Extension Flags
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
            
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://accounts.google.com/signin")
        
        try:
            page.wait_for_selector('input[type="email"]', timeout=8000)
            print(f"[{username}] Google hesabı ekranı açıldı, mail giriliyor...")
            # İnsan gibi yazma gecikmesi (delay) ekliyoruz
            page.type('input[type="email"]', username, delay=120)
            page.keyboard.press('Enter')
            
            time.sleep(3)
            page.wait_for_selector('input[type="password"]', timeout=10000)
            time.sleep(1) # Kısa bir insani duraksama
            print(f"[{username}] Şifre giriliyor...")
            page.type('input[type="password"]', password, delay=150)
            page.keyboard.press('Enter')
            
            print(f"[{username}] Google giriş adımları tamamlandı.")
            time.sleep(5)
            # Google logini sonrası asıl görev olan Twitter'a veya ana sekmeye yönel
            page.goto("https://twitter.com/")
        except Exception:
            print(f"[{username}] Zaten oturum açık olabilir veya ek güvenlik (telefon) onayı gerekiyor.")
            # Her ihtimale karşı oturum zaten açıksa da Twitter sayfasına devam edelim
            page.goto("https://twitter.com/")
            
        print(f"[{username}] Worker çalışıyor. Çıkmak için işlemi sonlandırın.")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            browser.close()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Kullanım: python worker.py <account_id> <username> <password> <profile_dir>")
        sys.exit(1)
        
    start_worker(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
