import os
import json
import subprocess
import sys

SESSIONS_FILE = "sessions.json"

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return []
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

def is_pid_alive(pid):
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            capture_output=True, text=True
        )
        return str(pid) in result.stdout
    except Exception:
        return False

def spawn_worker(email, password, profile_dir, mode="login"):
    log = open("worker_log.txt", "a", encoding="utf-8")
    proc = subprocess.Popen(
        [sys.executable, "worker.py", email, password, profile_dir, mode],
        stdout=log,
        stderr=log
    )
    return proc.pid

def menu_add_session():
    email = input("Google Mail Adresi: ").strip()
    password = input("Şifre: ").strip()
    if not email or not password:
        print("Mail ve şifre boş bırakılamaz.")
        return
    profile_dir = os.path.join(
        os.getcwd(), "profiles", email.replace("@", "_").replace(".", "_")
    )
    os.makedirs(profile_dir, exist_ok=True)
    sessions = load_sessions()
    for s in sessions:
        if s["email"] == email:
            print(f"Bu e-posta zaten kayıtlı: {email}")
            return
    pid = spawn_worker(email, password, profile_dir, mode="login")
    sessions.append({"email": email, "profile_dir": profile_dir, "pid": pid})
    save_sessions(sessions)
    print(f"Oturum başlatıldı → {email} (PID: {pid})")

def menu_list_sessions():
    sessions = load_sessions()
    if not sessions:
        print("Kayıtlı oturum yok.")
        return
    print("\n--- Kayıtlı Oturumlar ---")
    for i, s in enumerate(sessions):
        alive = is_pid_alive(s.get("pid", 0))
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
    save_sessions(sessions)
    sil = input(f"Profil dosyaları da silinsin mi? ({s['email']}) [e/h]: ").lower()
    if sil == "e":
        import shutil
        shutil.rmtree(s["profile_dir"], ignore_errors=True)
        print("Profil silindi.")
    print(f"Oturum kaldırıldı: {s['email']}")

def menu_open_sessions():
    sessions = load_sessions()
    if not sessions:
        print("Açılacak kayıtlı oturum yok.")
        return
    print("\n--- Mevcut Oturumlar ---")
    for i, s in enumerate(sessions):
        print(f"  [{i+1}] {s['email']}")
    print("  [0] Tümünü aç")
    try:
        sec = int(input("Seçim: "))
    except ValueError:
        return

    if sec == 0:
        targets = sessions
    elif 1 <= sec <= len(sessions):
        targets = [sessions[sec - 1]]
    else:
        print("Geçersiz seçim.")
        return

    for s in targets:
        if is_pid_alive(s.get("pid", 0)):
            print(f"Zaten açık: {s['email']}")
            continue
        pid = spawn_worker(s["email"], "", s["profile_dir"], mode="resume")
        s["pid"] = pid
        print(f"Oturum açıldı → {s['email']} (PID: {pid})")

    save_sessions(sessions)

def main():
    while True:
        print("\n=== Twitter Otomasyon Merkezi ===")
        print("1. Yeni Oturum Ekle")
        print("2. Oturumları Listele")
        print("3. Oturum Sil")
        print("4. Kayıtlı Oturumları Aç")
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
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim.")

        input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
