import sys
import json
import time
import os
import subprocess

from account_manager import (
    get_available_account,
    login_account,
    release_account,
    get_all_sessions,
    add_account,
    get_all_accounts,
    register_session
)
from browser_manager import start_session, stop_session
from setup_browser import setup_ungoogled_chromium

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Sistem gereksinimleri kontrol ediliyor...")
    setup_ungoogled_chromium()
    
    print("Dinamik betik sunucusu başlatılıyor...")
    api_server = subprocess.Popen([sys.executable, "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    try:
        while True:
            clear_screen()
            print("=== Twitter Otomasyon Merkezi ===")
            print("1. Yeni Oturum Aç ve Eklentiyi Çalıştır")
            print("2. Seçili Oturumu Kapat ve Hesabı Boşa Çıkar")
            print("3. Çalışan Betiği Güncelle ve Çalıştır")
            print("4. Hesap Ekle")
            print("5. Tüm Hesapları Görüntüle")
            print("0. Çıkış")
            print("================================")
            
            choice = input("Seçiminiz: ")
            
            if choice == '1':
                username = input("Google Mail Adresi: ")
                password = input("Şifresi: ")
                
                if not username or not password:
                    print("Uyarı: Mail ve Şifre boş bırakılamaz!")
                    input("Devam etmek için Enter'a basın...")
                    continue
                    
                account = login_account(username, password)
                acc_id, username, password = account
                print(f"[{username}] için oturum başlatılıyor...")
                pid = start_session(acc_id, username, password)
                if pid:
                    register_session(acc_id, pid)
                    print(f"Oturum başlatıldı! İşlem ID: {pid}")
                else:
                    release_account(acc_id)
                    print("Oturum başlatılamadı.")
                input("Devam etmek için Enter'a basın...")
                
            elif choice == '2':
                sessions = get_all_sessions()
                if not sessions:
                    print("Aktif oturum bulunamadı.")
                    input("Devam etmek için Enter'a basın...")
                    continue
                
                print("\nAktif Oturumlar:")
                for s in sessions:
                    print(f"Session ID: {s[0]} | Kullanıcı: {s[1]} | PID: {s[2]} | Hesap ID: {s[3]}")
                    
                try:
                    s_id = int(input("\nKapatılacak Session ID: "))
                    selected_session = next((x for x in sessions if x[0] == s_id), None)
                    if selected_session:
                        pid = selected_session[2]
                        acc_id = selected_session[3]
                        stop_session(pid)
                        release_account(acc_id)
                        print(f"Oturum ({pid}) kapatıldı. Hesap '{selected_session[1]}' boşa çıkarıldı.")
                    else:
                        print("Geçersiz Session ID.")
                except ValueError:
                    print("Hatalı giriş.")
                input("Devam etmek için Enter'a basın...")
                
            elif choice == '3':
                print("Yeni betiğin yolunu veya adını girin (Örn: scripts/yeni_betik.js)")
                new_script = input("Yol: ")
                
                try:
                    with open(new_script, 'r', encoding='utf-8') as f:
                        script_content = f.read()
                        
                    with open('current_script.js', 'w', encoding='utf-8') as target:
                        target.write(script_content)
                    print("Betik başarıyla güncellendi!")
                except FileNotFoundError:
                    print("Belirtilen dosya bulunamadı.")
                except Exception as e:
                    print(f"Bilinmeyen hata: {e}")
                input("Devam etmek için Enter'a basın...")

            elif choice == '4':
                username = input("Twitter Kullanıcı Adı: ")
                password = input("Twitter Şifresi: ")
                add_account(username, password)
                input("Devam etmek için Enter'a basın...")
                
            elif choice == '5':
                accs = get_all_accounts()
                for a in accs:
                    print(f"ID: {a[0]} | K.Adı: {a[1]} | Durum: {a[2]}")
                input("Devam etmek için Enter'a basın...")
                
            elif choice == '0':
                print("Çıkış yapılıyor...")
                api_server.terminate()
                break
            else:
                print("Geçersiz seçim.")
                input("Devam etmek için Enter'a basın...")
                
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
    finally:
        api_server.terminate()

if __name__ == '__main__':
    main()
