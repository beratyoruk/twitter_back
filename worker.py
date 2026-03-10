import os
import sys
import time
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def skip_optional_prompts(page):
    """Google'ın opsiyonel adımlarını (ev adresi, telefon, gizlilik) atlar."""
    skip_texts = ["Skip", "Not now", "Atla", "Şimdi değil", "Continue", "Devam et", "Remind me later"]
    for _ in range(5):
        time.sleep(2)
        skipped = False
        for text in skip_texts:
            try:
                btn = page.locator(f"text={text}").first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    skipped = True
                    time.sleep(1)
                    break
            except Exception:
                pass
        if not skipped:
            break

def open_twitter_tab(browser):
    page = browser.new_page()
    page.goto("https://twitter.com/")
    return page

def login_mode(browser, email, password):
    page = browser.pages[0] if browser.pages else browser.new_page()
    stealth_sync(page)
    page.goto("https://accounts.google.com/signin")

    try:
        page.wait_for_selector('input[type="email"]', timeout=10000)
        page.type('input[type="email"]', email, delay=120)
        page.keyboard.press("Enter")

        time.sleep(3)
        page.wait_for_selector('input[type="password"]', timeout=10000)
        time.sleep(1)
        page.type('input[type="password"]', password, delay=150)
        page.keyboard.press("Enter")

        print(f"[{email}] Giriş yapıldı. Opsiyonel adımlar atlanıyor...")
        time.sleep(3)
        skip_optional_prompts(page)

        # Google'dan çıkıldıktan sonra Twitter'ı aynı pencerede yeni sekmede aç
        print(f"[{email}] Twitter açılıyor...")
        twitter_page = open_twitter_tab(browser)
        stealth_sync(twitter_page)
        print(f"[{email}] Oturum aktif.")
    except Exception as e:
        print(f"[{email}] Giriş sırasında hata: {e}")
        try:
            open_twitter_tab(browser)
        except Exception:
            pass

def resume_mode(browser, email):
    """Kayıtlı profil çerezleriyle Twitter'ı doğrudan açar, yeniden giriş yapmaz."""
    page = browser.pages[0] if browser.pages else browser.new_page()
    stealth_sync(page)
    print(f"[{email}] Mevcut oturum yükleniyor...")
    page.goto("https://twitter.com/")
    print(f"[{email}] Oturum aktif.")

def run():
    if len(sys.argv) < 5:
        print("Kullanım: python worker.py <email> <password> <profile_dir> <mode>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    profile_dir = sys.argv[3]
    mode = sys.argv[4]

    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

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

        if mode == "login":
            login_mode(browser, email, password)
        else:
            resume_mode(browser, email)

        # Tüm sekmeler kapanana kadar bekle
        try:
            while browser.pages:
                time.sleep(2)
        except Exception:
            pass

if __name__ == "__main__":
    run()
