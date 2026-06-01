import sqlite3

class Database:
    """
    Класс для работы с SQLite базой данных пользователей.
    
    Обеспечивает создание таблицы пользователей, добавление новых записей
    и получение данных о пользователе. Каждый запрос создаёт новое соединение
    для обеспечения потокобезопасности.
    
    Атрибуты:
        db_path (str): Путь к файлу SQLite базы данных
    """
    
    def __init__(self, db_path="database.db"):
        """
        Инициализация обработчика базы данных.
        
        Аргументы:
            db_path (str): Путь к файлу базы данных. По умолчанию "database.db"
            
        Примечание:
            Автоматически создаёт таблицу users, если она не существует.
        """
        self.db_path = db_path
        self.init_db()

    def connection(self):
        """
        Создание нового соединения с базой данных.
        
        Возвращает:
            sqlite3.Connection: Объект соединения SQLite
            
        Примечание:
            Каждый вызов создаёт отдельное соединение, что упрощает управление
            транзакциями и избегает проблем с конкурентным доступом.
        """
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """
        Инициализация структуры базы данных.
        
        Создаёт таблицу 'users' со следующей схемой:
            - id: Первичный ключ, автоинкремент
            - username: Имя пользователя (уникальное, не может быть NULL)
            - password_hash: Хеш пароля (текст, не может быть NULL)
            - salt: Соль для безопасного хеширования (может быть NULL)
            - is_safe: Флаг безопасного хеширования (0 - SHA-256, 1 - bcrypt)
            
        Примечание:
            Если таблица уже существует, команда CREATE TABLE IF NOT EXISTS
            не вызовет ошибку и не изменит существующую структуру.
        """
        conn = self.connection()
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
        conn.close()

    def add_user(self, username, password_hash, salt, is_safe):
        """
        Добавление нового пользователя в базу данных.
        
        Аргументы:
            username (str): Имя пользователя (должно быть уникальным)
            password_hash (str): Хешированный пароль
            salt (str or None): Соль (для bcrypt) или None (для SHA-256)
            is_safe (bool or int): True/1 для bcrypt, False/0 для SHA-256
            
        Вызывает исключения:
            sqlite3.IntegrityError: Если пользователь с таким username уже существует
            
        Примечание:
            Значение is_safe преобразуется в целое число (0 или 1) для хранения в SQLite.
            Соединение автоматически закрывается в блоке finally для гарантии освобождения ресурсов.
        """
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt, is_safe)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, salt, int(is_safe)))
            conn.commit()
        finally:
            conn.close()

    def fetch_user(self, username):
        """
        Получение данных пользователя из базы данных по имени.
        
        Аргументы:
            username (str): Имя пользователя для поиска
            
        Возвращает:
            tuple or None: Кортеж (password_hash, salt, is_safe) если пользователь найден,
                          иначе None
                          
        Примечание:
            Не возвращает id пользователя, так как он не требуется для аутентификации.
            Соединение автоматически закрывается для предотвращения утечек.
        """
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash, salt, is_safe
                FROM users
                WHERE username = ?
            """, (username,))
            return cursor.fetchone()
        finally:
            conn.close()