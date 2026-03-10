import os
import json
import urllib.request
import subprocess

CONFIG_FILE = "config.json"
INSTALL_DIR = os.path.join(os.getcwd(), "ungoogled_chromium")

def get_latest_portapps_url():
    url = "https://api.github.com/repos/portapps/ungoogled-chromium-portable/releases/latest"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        for asset in data.get("assets", []):
            if asset["name"].endswith("setup.exe"):
                return asset["browser_download_url"]
    except Exception as e:
        print(f"Sürüm bilgisi alınamadı: {e}")
    return None

def setup_ungoogled_chromium():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {"chromium_path": "", "extension_path": "extension"}
        
    chromium_path = config.get("chromium_path", "")
    if chromium_path and os.path.exists(chromium_path):
        return chromium_path

    # Beklenen .exe yolu (Portapps chromium için)
    target_exe = os.path.join(INSTALL_DIR, "app", "chrome.exe")
    if os.path.exists(target_exe):
        config["chromium_path"] = target_exe
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return target_exe

    print("Ungoogled Chromium cihazda bulunamadı.")
    print("Otomatik olarak portapps üzerinden indiriliyor (Bu işlem internet hızınıza bağlı olarak birkaç dakika sürebilir)...")
    
    setup_url = get_latest_portapps_url()
    if not setup_url:
        print("Hata: İndirme linki GitHub üzerinden bulunamadı.")
        return None
        
    installer_path = os.path.join(os.getcwd(), "ungoogled_installer.exe")
    
    try:
        req = urllib.request.Request(setup_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(installer_path, 'wb') as out_file:
            out_file.write(response.read())
        print("İndirme tamamlandı.")
    except Exception as e:
        print(f"İndirme sırasında hata oluştu: {e}")
        return None
    
    print("Sessiz kurulum yapılıyor, lütfen bekleyin...")
    try:
        # Portapps Inno Setup veya NSIS kullanabilir. Sessiz kurulum argümanları:
        # Inno Setup için: /VERYSILENT /DIR="x"
        # NSIS için: /S /D=x
        # İkisini de deneriz ya da Portapps'in NSIS kullandığını biliyoruz (/S /D=...)
        # Aslında portapps NSIS kullanıyor (Makina InnoSetup). 
        # Hemen test edelim, hata vermeden kurmasını bekleriz.
        subprocess.run([installer_path, "/S", f"/D={INSTALL_DIR}"], check=True)
        
        config["chromium_path"] = target_exe
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
            
        print("Kurulum başarıyla tamamlandı!")
        return target_exe
    except Exception as e:
        print(f"Kurulum sırasında hata oluştu: {e}")
        return None
    finally:
        if os.path.exists(installer_path):
            try:
                os.remove(installer_path)
            except:
                pass

if __name__ == "__main__":
    path = setup_ungoogled_chromium()
    if path:
        print(f"Tarayıcı Hazır: {path}")
