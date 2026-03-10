import os
import sys
import time
import json
import subprocess
from playwright.sync_api import sync_playwright

CONFIG_FILE = "config.json"

STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'languages', {get: () => ['tr-TR', 'tr', 'en-US', 'en']});
Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
window.chrome = {runtime: {}};
"""

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def apply_stealth(page):
    page.add_init_script(STEALTH_SCRIPT)

def open_chrome_for_login(chrome_path, profile_dir, extension_path):
    """
    Ungoogled Chromium'u Playwright olmadan, doğrudan subprocess ile açar.
    Google gerçek bir tarayıcı görür, bot tespiti yaşanmaz.
    """
    args = [
        chrome_path,
        f"--user-data-dir={profile_dir}",
        f"--load-extension={extension_path}",
        "--start-maximized",
        "--no-default-browser-check",
        "--disable-search-engine-collection",
        "--disable-encryption",
        "--disable-machine-id",
        "https://accounts.google.com/signin",
    ]
    proc = subprocess.Popen(args)
    return proc

def login_mode(email, profile_dir, config):
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

    if not chrome_path or not os.path.exists(chrome_path):
        print("HATA: config.json içinde chromium_path doğru ayarlanmamış.")
        return

    print(f"\n[{email}] Tarayıcı açılıyor (Google girişi için)...")
    print("→ Google hesabına giriş yapın.")
    print("→ Tüm adımları tamamladıktan sonra bu terminale dönüp Enter'a basın.")

    proc = open_chrome_for_login(chrome_path, profile_dir, extension_path)
    input("\n[Enter] Giriş tamamlandı, devam ediliyor...")

    # Tarayıcıyı kapat (profil kaydedildi)
    try:
        proc.terminate()
        time.sleep(1)
    except Exception:
        pass

    print(f"[{email}] Profil kaydedildi. Artık 'Oturumları Aç' ile açılabilir.")

def resume_mode(browser, email):
    """Kayıtlı profil çerezleriyle Twitter'ı doğrudan açar."""
    page = browser.pages[0] if browser.pages else browser.new_page()
    apply_stealth(page)
    print(f"[{email}] Mevcut oturum yükleniyor...")
    page.goto("https://twitter.com/")
    print(f"[{email}] Oturum aktif.")

def run():
    if len(sys.argv) < 5:
        print("Kullanım: python worker.py <email> <password> <profile_dir> <mode>")
        sys.exit(1)

    email    = sys.argv[1]
    password = sys.argv[2]
    profile_dir = sys.argv[3]
    mode     = sys.argv[4]

    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

    if mode == "login":
        login_mode(email, profile_dir, config)
        return

    # resume modu: Playwright ile aç
    args = [
        "--disable-beforeunload",
        "--disable-search-engine-collection",
        "--fingerprinting-canvas-image-data-noise",
        "--fingerprinting-canvas-measuretext-noise",
        "--fingerprinting-client-rects-noise",
        "--hide-crashed-bubble",
        "--keep-old-history",
        "--max-connections-per-host=15",
        "--popups-to-tabs",
        "--disable-encryption",
        "--disable-machine-id",
        "--disable-sharing-hub",
        "--remove-tabsearch-button",
        "--disable-top-sites",
        "--no-default-browser-check",
        "--no-pings",
        "--webrtc-ip-handling-policy=default_public_interface_only",
        "--enable-features=MinimalReferrers,NoCrossOriginReferrers,ReducedSystemInfo,RemoveClientHints,SpoofWebGLInfo",
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        f"--disable-extensions-except={extension_path}",
        f"--load-extension={extension_path}",
    ]

    with sync_playwright() as p:
        kwargs = {
            "user_data_dir": profile_dir,
            "headless": False,
            "args": args,
        }
        if chrome_path and os.path.exists(chrome_path):
            kwargs["executable_path"] = chrome_path

        browser = p.chromium.launch_persistent_context(**kwargs)
        resume_mode(browser, email)

        try:
            while browser.pages:
                time.sleep(2)
        except Exception:
            pass

if __name__ == "__main__":
    run()
