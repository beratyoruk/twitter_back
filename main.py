import os
import time
import json
from playwright.sync_api import sync_playwright

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def run():
    email = input("Google Mail Adresi: ")
    password = input("Şifre: ")

    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))
    profile_dir = os.path.join(os.getcwd(), "profiles", email.replace("@", "_").replace(".", "_"))
    os.makedirs(profile_dir, exist_ok=True)

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

        print("Tarayıcı açılıyor...")
        browser = p.chromium.launch_persistent_context(**kwargs)
        page = browser.pages[0] if browser.pages else browser.new_page()
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

            print("Giriş yapıldı. 2FA/SMS gerekiyorsa lütfen tarayıcıda tamamlayın...")
            page.wait_for_url(lambda url: "accounts.google.com" not in url, timeout=0)

            print("Giriş tamamlandı. Twitter'a yönlendiriliyor...")
            page.goto("https://twitter.com/")
        except Exception:
            print("Giriş zaten yapılmış veya ek adım gerekiyor. Devam ediliyor...")
            try:
                page.goto("https://twitter.com/")
            except Exception:
                pass

        print("Oturum aktif. Pencereyi kapattığınızda program sonlanır.")
        try:
            browser.wait_for_event("close", timeout=0)
        except Exception:
            pass

if __name__ == "__main__":
    run()
