import sqlite3

class Database:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.init_db()

    
    def connection(self):
        return sqlite3.connect(self.db_path)
    

    def init_db(self):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT,
                    is_safe INTEGER NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()


    def add_user(self, username, password_hash, salt, is_safe):
        conn = self.connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt, is_safe) VALUES (?, ?, ?, ?)",
                    (username, password_hash, salt, int(is_safe))
                )
        finally:
            conn.close()


    def fetch_user(self, username):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt, is_safe FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
        finally:
            conn.close()
        
    
    def close(self):
        pass