import sqlite3

def init_database(path):
    """Создание БД"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                    (login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL)
                    """)
    conn.commit()
    conn.close()


def add_user(path,login,password,salt):
    """Добавление пользователя в БД"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (login,password,salt) VALUES (?,?,?)",(login,password,salt))
    conn.commit()
    conn.close()

def get_data(path,username):
    """Получение информации о пользователе из БД"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT password,salt FROM users WHERE login=?",(username,))
    result=cursor.fetchall()
    conn.close()
    return result
