import sqlite3


def initSQL(db_path: str):
    """
    Create database file and table if it is not exists

    :param db_path: Path to db file
    :type db_path: str
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, salt TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()


def register_user(username: str, password_hash: bytes, salt: bytes, db_path: str):
    """
    Added new user data to users table in database file

    :param username: Username for table
    :type username: str
    :param password_hash: Hash of password for table
    :type password_hash: bytes
    :param salt: User salt for table
    :type salt: bytes
    :param db_path: Path to db file
    :type db_path: str
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO users (username, password_hash, salt) VALUES ('{username}', '{password_hash.hex()}', '{salt.hex()}')"
        )

        conn.commit()
    except sqlite3.IntegrityError:
        raise sqlite3.IntegrityError
    except Exception as e:
        raise e
    finally:
        conn.close()


def get_user(username: str, db_path: str):
    """
    Get user data from database file

    :param username: Username to get data
    :type username: str
    :param db_path: Path to db file
    :type db_path: str
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT password_hash, salt FROM users WHERE username='{username}'")
    result = cursor.fetchone()
    conn.close()
    return result
