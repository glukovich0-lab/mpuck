import sqlite3

def init_db():
    conn = sqlite3.connect("mpuck.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            invite_code TEXT,
            is_verified INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def verify_user(tg_id, code):
    conn = sqlite3.connect("mpuck.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE invite_code=?", (code,))
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE users SET tg_id=?, is_verified=1 WHERE invite_code=?",
            (tg_id, code)
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def is_verified(tg_id):
    conn = sqlite3.connect("mpuck.db")
    cur = conn.cursor()

    cur.execute("SELECT is_verified FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()

    conn.close()
    return row and row[0] == 1
