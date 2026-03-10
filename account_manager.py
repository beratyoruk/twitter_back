import sqlite3

DB_PATH = 'db.sqlite3'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            status TEXT DEFAULT 'available'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            pid INTEGER,
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_account(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"Hesap eklendi: {username}")
    except sqlite3.IntegrityError:
        print(f"Hesap zaten mevcut: {username}")
    finally:
        conn.close()

def get_available_account():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM accounts WHERE status = 'available' LIMIT 1")
    account = cursor.fetchone()
    if account:
        cursor.execute("UPDATE accounts SET status = 'in_use' WHERE id = ?", (account[0],))
        conn.commit()
    conn.close()
    return account

def release_account(account_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET status = 'available' WHERE id = ?", (account_id,))
    cursor.execute("DELETE FROM sessions WHERE account_id = ?", (account_id,))
    conn.commit()
    conn.close()

def register_session(account_id, pid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (account_id, pid) VALUES (?, ?)", (account_id, pid))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, a.username, s.pid, a.id as account_id
        FROM sessions s
        JOIN accounts a ON s.account_id = a.id
    ''')
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def get_all_accounts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, status FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts

init_db()
