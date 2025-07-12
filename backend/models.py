import sqlite3

def create_tables():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Subscriptions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER,
            plan TEXT DEFAULT 'free',
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Chats table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Admin settings table
c.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        site_name TEXT DEFAULT 'Luna Ai',
        theme TEXT DEFAULT 'Dark',
        logo TEXT DEFAULT '/static/logo.png'
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")


# Optional: insert default row
c.execute("INSERT INTO settings (site_name, theme, logo) VALUES ('Luna Ai', 'Dark', '/static/logo.png')")

    conn.commit()
    conn.close()
