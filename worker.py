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
        page.goto("https://twitter.com/login")
        
        try:
            page.wait_for_selector('input[autocomplete="username"]', timeout=5000)
            page.fill('input[autocomplete="username"]', username)
            page.keyboard.press('Enter')
            
            page.wait_for_selector('input[name="password"]', timeout=5000)
            page.fill('input[name="password"]', password)
            page.keyboard.press('Enter')
            
            print(f"[{username}] Worker giriş denemesini tamamladı.")
        except Exception:
            pass
            
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
