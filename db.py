import sqlite3
from datetime import datetime
from config import ADMIN_ID

DB_NAME = "database.db"

# Asosiy admin ID sini har doim integerga o'giramiz
MAIN_ADMIN_ID = int(ADMIN_ID)


def get_connection():
    # Database is locked xatosini oldini olish uchun timeout qo'shildi
    return sqlite3.connect(DB_NAME, timeout=10.0)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        lang TEXT DEFAULT 'latin',
        is_blocked INTEGER DEFAULT 0,
        joined_at TEXT
    )
    """)

    # Groups jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        title TEXT
    )
    """)

    # Admins jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY
    )
    """)

    # Ads (reklama) xabarlarini saqlash
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sent_ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT OR IGNORE INTO users (user_id, joined_at) VALUES (?, ?)", (user_id, now))
    cursor.execute("UPDATE users SET is_blocked = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def set_user_lang(user_id: int, lang: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()


def get_user_lang(user_id: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else 'latin'


def add_group(group_id: int, title: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO groups (group_id, title) VALUES (?, ?)", (group_id, title))
    conn.commit()
    conn.close()


def get_all_groups():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT group_id, title FROM groups")
    res = cursor.fetchall()
    conn.close()
    return res


def set_user_blocked(user_id: int, is_blocked: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_blocked = ? WHERE user_id = ?", (is_blocked, user_id))
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    res = [r[0] for r in cursor.fetchall()]
    conn.close()
    return res


def get_user_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE is_blocked = 1")
    blocked = cursor.fetchone()[0]

    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM users WHERE joined_at LIKE ?", (f"{today_str}%",))
    today = cursor.fetchone()[0]

    year_str = datetime.now().strftime("%Y")
    cursor.execute("SELECT COUNT(*) FROM users WHERE joined_at LIKE ?", (f"{year_str}%",))
    year = cursor.fetchone()[0]

    month_str = datetime.now().strftime("%Y-%m")
    cursor.execute("SELECT COUNT(*) FROM users WHERE joined_at LIKE ?", (f"{month_str}%",))
    month = cursor.fetchone()[0]

    conn.close()
    return {
        "total": total,
        "blocked": blocked,
        "today": today,
        "week": today,
        "month": month,
        "year": year
    }


def add_admin(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def remove_admin(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True


# Chaqirishda 1 ta argument yuborilishi uchun parametri soddalashtirildi
def is_admin(user_id: int) -> bool:
    if int(user_id) == MAIN_ADMIN_ID:
        return True
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res is not None


def save_sent_ad(user_id: int, message_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sent_ads (user_id, message_id) VALUES (?, ?)", (user_id, message_id))
    conn.commit()
    conn.close()


def get_and_clear_last_ads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, message_id FROM sent_ads")
    ads = cursor.fetchall()
    cursor.execute("DELETE FROM sent_ads")
    conn.commit()
    conn.close()
    return ads