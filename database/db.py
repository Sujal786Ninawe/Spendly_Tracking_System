import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "spendly.db"


def get_db():
    """Open connection to SQLite database with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TEXT DEFAULT (datetime('now')))")

    # Create expenses table
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, date TEXT NOT NULL, description TEXT, created_at TEXT DEFAULT (datetime('now')), FOREIGN KEY (user_id) REFERENCES users(id))")

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development (safe to call multiple times)."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Already seeded

    # Create demo user
    password_hash = generate_password_hash("demo123")
    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", ("Demo User", "demo@spendly.com", password_hash))

    conn.commit()
    conn.close()
