import subprocess
import os

WORKER_SCRIPT = "worker.py"

def start_session(account_id, username, password):
    profile_dir = os.path.join(os.getcwd(), "profiles", f"profile_{username}")
    os.makedirs(profile_dir, exist_ok=True)
    
    process = subprocess.Popen(
        ["python", WORKER_SCRIPT, str(account_id), username, password, profile_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return process.pid

def stop_session(pid):
    try:
        if os.name == 'nt':
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)])
        else:
            os.kill(pid, 9)
        return True
    except Exception as e:
        print(f"Oturum sonlandırılamadı: {e}")
        return False
