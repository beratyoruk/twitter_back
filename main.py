import os
import json
import sqlite3
import subprocess
import sys
import time
import shutil
import threading
import pyautogui

DB_FILE = "sessions.db"
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

# ─── Database ───────────────────────────────────────────────────────────────

def db_connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def db_init():
    with db_connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                profile_dir TEXT NOT NULL,
                status TEXT DEFAULT 'closed',
                pid INTEGER
            )
        """)

def db_all():
    with db_connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM sessions ORDER BY id")]

def db_get(email):
    with db_connect() as conn:
        r = conn.execute("SELECT * FROM sessions WHERE email=?", (email,)).fetchone()
        return dict(r) if r else None

def db_add(email, profile_dir):
    with db_connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO sessions (email, profile_dir, status, pid) VALUES (?,?,?,?)",
            (email, profile_dir, "closed", None)
        )

def db_delete(session_id):
    with db_connect() as conn:
        conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))

def db_set_status(session_id, status, pid=None):
    with db_connect() as conn:
        conn.execute(
            "UPDATE sessions SET status=?, pid=? WHERE id=?",
            (status, pid, session_id)
        )

# ─── Config ─────────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

# ─── Process ────────────────────────────────────────────────────────────────

def is_pid_alive(pid):
    if not pid:
        return False
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             f"(Get-Process -Id {pid} -ErrorAction SilentlyContinue) -ne $null"],
            capture_output=True, text=True, timeout=4
        )
        return result.stdout.strip().lower() == "true"
    except Exception:
        return False

def find_chrome_pid(profile_dir):
    """profile_dir ile eşleşen chrome.exe sürecinin PID'ini döner."""
    try:
        base = os.path.basename(profile_dir)
        cmd = (
            f"Get-WmiObject Win32_Process | "
            f"Where-Object {{$_.Name -eq 'chrome.exe' -and $_.CommandLine -like '*{base}*'}} | "
            f"Sort-Object WorkingSetSize -Descending | "
            f"Select-Object -First 1 -ExpandProperty ProcessId"
        )
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True, text=True, timeout=6
        )
        pid_str = result.stdout.strip()
        return int(pid_str) if pid_str.isdigit() else None
    except Exception:
        return None

def kill_pid(pid):
    if not pid:
        return
    try:
        subprocess.run(
            ["powershell", "-Command", f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"],
            capture_output=True, timeout=5
        )
    except Exception:
        pass

def launch_browser(chrome_path, profile_dir, extension_path, urls):
    if isinstance(urls, str):
        urls = [urls]
    args = [chrome_path, f"--user-data-dir={profile_dir}", f"--load-extension={extension_path}"] + CHROME_FLAGS + urls
    proc = subprocess.Popen(args)
    time.sleep(2.5)
    real_pid = find_chrome_pid(profile_dir) or proc.pid
    return real_pid

# ─── Background Monitor ──────────────────────────────────────────────────────

def monitor_sessions():
    """Her 10 saniyede açık oturumları kontrol eder, kapananları DB'de kapalı işaretler."""
    while True:
        time.sleep(10)
        try:
            sessions = db_all()
            for s in sessions:
                if s["status"] == "open":
                    if not is_pid_alive(s["pid"]):
                        db_set_status(s["id"], "closed", None)
        except Exception:
            pass

# ─── Human Typing ────────────────────────────────────────────────────────────

def human_type(text):
    import random
    from pynput.keyboard import Controller as KB
    kb = KB()
    for ch in text:
        kb.type(ch)
        time.sleep(random.uniform(0.07, 0.15))

def wait_window(keywords, timeout=20):
    import pygetwindow as gw
    deadline = time.time() + timeout
    while time.time() < deadline:
        for title in gw.getAllTitles():
            if any(k in title.lower() for k in keywords):
                return title
        time.sleep(0.5)
    return None

def activate_win(title):
    import pygetwindow as gw
    try:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].restore()
            wins[0].activate()
            time.sleep(1.2)
    except Exception:
        pass

def auto_google_login(email, password):
    from pynput.keyboard import Controller as KB, Key
    sw, sh = pyautogui.size()

    print("  → Giriş sayfası yükleniyor...")
    title = wait_window(["chromium", "chrome", "google", "accounts", "sign", "oturum", "giriş"])
    if not title:
        print("  ! Pencere bulunamadı, manuel giriş yapın.")
        return

    activate_win(title)
    time.sleep(1.5)

    # Email alanını tıkla (dikey ~%42)
    pyautogui.moveTo(sw // 2, int(sh * 0.42), duration=0.4)
    pyautogui.click()
    time.sleep(0.8)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)

    print("  → E-posta yazılıyor...")
    human_type(email)
    time.sleep(0.4)
    KB().press(Key.enter)
    KB().release(Key.enter)

    # Şifre sayfasının yüklenmesini bekle
    print("  → Şifre sayfası yükleniyor...")
    time.sleep(4)

    # Şifre alanını tıkla (dikey ~%48)
    pyautogui.moveTo(sw // 2, int(sh * 0.48), duration=0.4)
    pyautogui.click()
    time.sleep(0.8)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)

    print("  → Şifre yazılıyor...")
    human_type(password)
    time.sleep(0.4)
    KB().press(Key.enter)
    KB().release(Key.enter)

    print("  → Giriş yapıldı. 2FA varsa tarayıcıda tamamlayıp Enter'a basın.")
    time.sleep(3)

# ─── Menu ────────────────────────────────────────────────────────────────────

def menu_add_session():
    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

    if not chrome_path or not os.path.exists(chrome_path):
        print("HATA: chromium_path config.json'da yanlış.")
        return

    email = input("Google Mail: ").strip()
    password = input("Şifre: ").strip()
    if not email or not password:
        return

    if db_get(email):
        print(f"Bu hesap zaten kayıtlı: {email}")
        return

    profile_dir = os.path.join(os.getcwd(), "profiles", email.replace("@", "_").replace(".", "_"))
    os.makedirs(profile_dir, exist_ok=True)

    print(f"\n→ Tarayıcı açılıyor: {email}")
    pid = launch_browser(chrome_path, profile_dir, extension_path, "https://accounts.google.com/signin")
    auto_google_login(email, password)

    input("\n[Enter] Giriş tamamlandı, devam et...")
    kill_pid(pid)

    db_add(email, profile_dir)
    print(f"✓ Oturum kaydedildi: {email}")

def menu_list():
    sessions = db_all()
    if not sessions:
        print("Kayıtlı oturum yok.")
        return
    print("\n--- Oturumlar ---")
    for s in sessions:
        durum = "🟢 Aktif" if s["status"] == "open" else "🔴 Kapalı"
        print(f"  [{s['id']}] {s['email']} — {durum}")
    print()

def menu_delete():
    sessions = db_all()
    if not sessions:
        print("Silinecek oturum yok.")
        return
    menu_list()
    try:
        sid = int(input("Silinecek ID: "))
    except ValueError:
        return

    s = next((x for x in sessions if x["id"] == sid), None)
    if not s:
        print("Geçersiz ID.")
        return

    # Tarayıcıyı kapat
    kill_pid(s.get("pid"))
    time.sleep(1)

    # DB'den sil
    db_delete(sid)

    # Profil klasörünü sil
    sil = input(f"Profil disk'ten de silinsin mi? ({s['email']}) [e/h]: ").lower()
    if sil == "e":
        shutil.rmtree(s["profile_dir"], ignore_errors=True)
        print("Profil silindi.")

    print(f"✓ {s['email']} tamamen kaldırıldı.")

def menu_open():
    sessions = db_all()
    if not sessions:
        print("Kayıtlı oturum yok.")
        return

    config = load_config()
    chrome_path = config.get("chromium_path", "")
    extension_path = os.path.abspath(config.get("extension_path", "extension"))

    menu_list()
    print("  [0] Tümünü aç")
    try:
        sec = int(input("Seçim: "))
    except ValueError:
        return

    if sec == 0:
        targets = sessions
    else:
        targets = [s for s in sessions if s["id"] == sec]
        if not targets:
            print("Geçersiz ID.")
            return

    for s in targets:
        if s["status"] == "open" and is_pid_alive(s["pid"]):
            print(f"Zaten açık: {s['email']}")
            continue
        pid = launch_browser(
            chrome_path, s["profile_dir"], extension_path,
            ["https://myaccount.google.com/", "https://twitter.com/"]
        )
        db_set_status(s["id"], "open", pid)
        print(f"✓ Açıldı: {s['email']} (Google + Twitter, PID:{pid})")

def main():
    db_init()
    t = threading.Thread(target=monitor_sessions, daemon=True)
    t.start()

    while True:
        print("\n=== Twitter Otomasyon Merkezi ===")
        print("1. Yeni Oturum Ekle (Otomatik Google Girişi)")
        print("2. Oturumları Listele")
        print("3. Oturum Sil (Tarayıcı + DB + Profil)")
        print("4. Kayıtlı Oturumları Aç (Google + Twitter)")
        print("0. Çıkış")
        print("=================================")

        choice = input("Seçim: ").strip()

        if choice == "1":
            menu_add_session()
        elif choice == "2":
            menu_list()
        elif choice == "3":
            menu_delete()
        elif choice == "4":
            menu_open()
        elif choice == "0":
            print("Çıkış.")
            break
        else:
            print("Geçersiz seçim.")

        input("\n[Enter] Ana menüye dön...")

if __name__ == "__main__":
    main()
