import os
import json
import subprocess
import sys
import time
import shutil
import pyautogui

SESSIONS_FILE = "sessions.json"
CONFIG_FILE = "config.json"

CHROME_FLAGS = [
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
    "--start-maximized",
]

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return []
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

def is_pid_alive(pid):
    if not pid:
        return False
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            capture_output=True, text=True
        )
        return str(pid) in result.stdout
    except Exception:
        return False

def launch_browser(chrome_path, profile_dir, extension_path, urls):
    """urls: tek string veya liste — birden fazla url = birden fazla sekme."""
    if isinstance(urls, str):
        urls = [urls]
    args = [chrome_path, f"--user-data-dir={profile_dir}", f"--load-extension={extension_path}"] + CHROME_FLAGS + urls
    proc = subprocess.Popen(args)
    return proc.pid

def focus_browser_window(timeout=12):
    """Chromium/Chrome penceresini bulur ve odağa alır."""
    import pygetwindow as gw
    deadline = time.time() + timeout
    while time.time() < deadline:
        for title in gw.getAllTitles():
            if any(k in title.lower() for k in ["chromium", "chrome", "google", "sign in", "accounts"]):
                try:
                    win = gw.getWindowsWithTitle(title)[0]
                    win.activate()
                    time.sleep(0.8)
                    return True
                except Exception:
                    pass
        time.sleep(0.5)
    return False

def auto_google_login(email, password):
    """
    OS seviyesinde klavye simülasyonu ile Google girişi yapar.
    pyautogui CDP kullanmaz — Google bot tespiti yapamaz.
    """
    print("  → Tarayıcı penceresi bekleniyor...")
    if not focus_browser_window(timeout=15):
        print("  ! Tarayıcı penceresi bulunamadı, manuel giriş yapın.")
        return

    print("  → E-posta giriliyor...")
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'a')
    import pyperclip
    pyperclip.copy(email)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.4)
    pyautogui.press('enter')

    print("  → Şifre bekleniyor...")
    time.sleep(3.5)
    pyperclip.copy(password)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.4)
    pyautogui.press('enter')

    print("  → Giriş gönderildi. 2FA varsa tarayıcıda tamamlayın.")
    time.sleep(4)



def menu_add_session():
    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

    if not chrome_path or not os.path.exists(chrome_path):
        print("HATA: config.json içinde chromium_path doğru ayarlanmamış.")
        return

    email = input("Google Mail Adresi: ").strip()
    password = input("Şifre: ").strip()
    if not email or not password:
        print("Mail ve şifre boş bırakılamaz.")
        return

    sessions = load_sessions()
    if any(s["email"] == email for s in sessions):
        print(f"Bu hesap zaten kayıtlı: {email}")
        return

    profile_dir = os.path.join(os.getcwd(), "profiles", email.replace("@", "_").replace(".", "_"))
    os.makedirs(profile_dir, exist_ok=True)

    print(f"\n→ Tarayıcı açılıyor: {email}")
    print("  Lütfen 5 saniye boyunca başka bir şeye tıklamayın!\n")

    pid = launch_browser(chrome_path, profile_dir, extension_path, "https://accounts.google.com/signin")
    auto_google_login(email, password)

    # 2FA varsa kullanıcı tamamlasın
    input("\n[Enter] Giriş tamamlandı, devam et...")

    try:
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
    except Exception:
        pass
    time.sleep(1)

    sessions.append({"email": email, "profile_dir": profile_dir, "pid": None})
    save_sessions(sessions)
    print(f"\n✓ Oturum kaydedildi: {email}")

def menu_list_sessions():
    sessions = load_sessions()
    if not sessions:
        print("Kayıtlı oturum yok.")
        return
    print("\n--- Kayıtlı Oturumlar ---")
    for i, s in enumerate(sessions):
        alive = is_pid_alive(s.get("pid"))
        durum = "🟢 Aktif" if alive else "🔴 Kapalı"
        print(f"  [{i+1}] {s['email']} — {durum}")
    print()

def menu_delete_session():
    sessions = load_sessions()
    if not sessions:
        print("Silinecek oturum yok.")
        return
    menu_list_sessions()
    try:
        idx = int(input("Silinecek oturum numarası (0=iptal): ")) - 1
    except ValueError:
        return
    if idx < 0 or idx >= len(sessions):
        return

    s = sessions.pop(idx)
    if is_pid_alive(s.get("pid")):
        subprocess.call(["taskkill", "/F", "/T", "/PID", str(s["pid"])])

    save_sessions(sessions)
    sil = input(f"Profil dosyaları da silinsin mi? ({s['email']}) [e/h]: ").lower()
    if sil == "e":
        shutil.rmtree(s["profile_dir"], ignore_errors=True)
        print("Profil silindi.")
    print(f"✓ Oturum kaldırıldı: {s['email']}")

def menu_open_sessions():
    sessions = load_sessions()
    if not sessions:
        print("Açılacak kayıtlı oturum yok.")
        return

    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

    if not chrome_path or not os.path.exists(chrome_path):
        print("HATA: config.json içinde chromium_path doğru ayarlanmamış.")
        return

    print("\n--- Kayıtlı Oturumlar ---")
    for i, s in enumerate(sessions):
        alive = is_pid_alive(s.get("pid"))
        durum = "🟢 Aktif" if alive else "🔴 Kapalı"
        print(f"  [{i+1}] {s['email']} — {durum}")
    print("  [0] Tümünü aç\n")

    try:
        sec = int(input("Seçim: "))
    except ValueError:
        return

    if sec == 0:
        targets = list(range(len(sessions)))
    elif 1 <= sec <= len(sessions):
        targets = [sec - 1]
    else:
        print("Geçersiz seçim.")
        return

    for idx in targets:
        s = sessions[idx]
        if is_pid_alive(s.get("pid")):
            print(f"Zaten açık: {s['email']}")
            continue
        # Profil çerezleri var → Google sekmesi + Twitter sekmesi aynı anda aç
        pid = launch_browser(
            chrome_path, s["profile_dir"], extension_path,
            ["https://myaccount.google.com/", "https://twitter.com/"]
        )
        sessions[idx]["pid"] = pid
        print(f"✓ Açıldı: {s['email']} (Google + Twitter — PID: {pid})")

    save_sessions(sessions)

def main():
    while True:
        print("\n=== Twitter Otomasyon Merkezi ===")
        print("1. Yeni Oturum Ekle (Otomatik Google Girişi)")
        print("2. Oturumları Listele")
        print("3. Oturum Sil")
        print("4. Kayıtlı Oturumları Aç (Google + Twitter)")
        print("0. Çıkış")
        print("=================================")

        choice = input("Seçim: ").strip()

        if choice == "1":
            menu_add_session()
        elif choice == "2":
            menu_list_sessions()
        elif choice == "3":
            menu_delete_session()
        elif choice == "4":
            menu_open_sessions()
        elif choice == "0":
            print("Çıkış.")
            break
        else:
            print("Geçersiz seçim.")

        input("\n[Enter] Ana menüye dön...")

if __name__ == "__main__":
    main()
