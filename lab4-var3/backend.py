import json
import hashlib
import secrets
import bcrypt
from tqdm import tqdm
from db import Database

class Auth:
    """
    Система аутентификации, поддерживающая небезопасное (SHA-256) и безопасное (bcrypt) хеширование паролей.
    
    Этот класс предоставляет функционал регистрации пользователей, проверки учётных данных
    и демонстрационный модуль для брутфорс-атаки, позволяющий сравнить безопасность
    между обычным SHA-256 и солированным bcrypt-хешированием.
    
    Атрибуты:
        settings (dict): Конфигурация, загруженная из JSON-файла, содержит:
            - db_path: Путь к файлу SQLite базы данных
            - salt_length: Длина случайной соли в байтах (в hex-кодировке)
            - bruteforce_iters: Количество итераций для демонстрации брутфорса
            - bcrypt_rounds: Фактор сложности для bcrypt (выше = медленнее)
        db (Database): Обработчик базы данных для хранения пользователей
    """
    
    def __init__(self, settings="settings.json", db_path=None):
        """
        Инициализация системы аутентификации с загрузкой конфигурации и подключением к БД.
        
        Аргументы:
            settings (str): Путь к JSON-файлу конфигурации. По умолчанию "settings.json".
            db_path (str, optional): Переопределённый путь к базе данных. 
                                     Если None, используется путь из настроек.
            
        Примечание:
            Если файл настроек не может быть загружен, используются значения по умолчанию
            для обеспечения работоспособности системы.
        """
        self.load_settings(settings)
        db_path = db_path or self.settings["db_path"]
        self.db = Database(db_path)

    def load_settings(self, path):
        """
        Загрузка конфигурации из JSON-файла.
        
        Аргументы:
            path (str): Путь к файлу settings.json
            
        Примечание:
            В случае ошибки (файл не найден, неверный JSON) инициализирует настройки
            по умолчанию, чтобы система продолжала функционировать.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except Exception:
            self.settings = {
                "db_path": "database.db",
                "salt_length": 16,
                "bruteforce_iters": 5000,
                "bcrypt_rounds": 12
            }

    def validate(self, u, p):
        """
        Проверка корректности введённых имени пользователя и пароля.
        
        Аргументы:
            u (str): Имя пользователя
            p (str): Пароль
            
        Возвращает:
            None: При успешной валидации
            
        Вызывает исключения:
            TypeError: Если u или p не являются строками
            ValueError: Если имя пользователя или пароль пустые (только пробелы)
        """
        if not isinstance(u, str) or not isinstance(p, str):
            raise TypeError("Invalid types")
        if not u.strip() or not p.strip():
            raise ValueError("Empty fields")

    def unsafe_hash(self, password):
        """
        Небезопасное хеширование пароля с помощью SHA-256 (без соли).
        
        Аргументы:
            password (str): Пароль в открытом виде
            
        Возвращает:
            str: Шестнадцатеричная строка хеша SHA-256
            
        Примечание:
            Этот метод уязвим для радужных таблиц и атак по словарю,
            так как одинаковые пароли дают одинаковые хеши.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def safe_hash(self, password, salt):
        """
        Безопасное хеширование пароля с использованием bcrypt.
        
        Аргументы:
            password (str): Пароль в открытом виде
            salt (str): Случайная соль, добавляемая к паролю перед хешированием
            
        Возвращает:
            str: bcrypt-хеш в кодировке Base64, содержащий соль и стоимость
            
        Примечание:
            bcrypt автоматически генерирует свою соль и включает её в результат.
            Внешняя соль используется для дополнительного уровня безопасности.
        """
        data = password + salt
        salt_b = bcrypt.gensalt(self.settings["bcrypt_rounds"])
        return bcrypt.hashpw(data.encode(), salt_b).decode()

    def generate_salt(self):
        """
        Генерация криптографически стойкой случайной соли.
        
        Возвращает:
            str: Шестнадцатеричная строка случайных байтов указанной длины
            
        Примечание:
            Используется secrets.token_hex() для криптографической безопасности,
            а не random модуль (который небезопасен для этой цели).
        """
        return secrets.token_hex(self.settings["salt_length"])

    def unsafe_registration(self, u, p):
        """
        Регистрация пользователя с небезопасным хешированием пароля (SHA-256).
        
        Аргументы:
            u (str): Имя пользователя
            p (str): Пароль в открытом виде
            
        Вызывает исключения:
            TypeError: При неверных типах данных
            ValueError: При пустых полях
            sqlite3.IntegrityError: Если пользователь с таким именем уже существует
            
        Примечание:
            Пароль хранится как обычный SHA-256 хеш без соли.
            Поле salt в БД устанавливается в NULL, is_safe = 0.
        """
        self.validate(u, p)
        self.db.add_user(u, self.unsafe_hash(p), None, False)

    def safe_registration(self, u, p):
        """
        Регистрация пользователя с безопасным хешированием пароля (bcrypt + соль).
        
        Аргументы:
            u (str): Имя пользователя
            p (str): Пароль в открытом виде
            
        Вызывает исключения:
            TypeError: При неверных типах данных
            ValueError: При пустых полях
            sqlite3.IntegrityError: Если пользователь с таким именем уже существует
            
        Примечание:
            Пароль комбинируется со случайной солью, затем хешируется bcrypt.
            Хранятся: bcrypt-хеш, соль, is_safe = 1.
        """
        self.validate(u, p)
        salt = self.generate_salt()
        self.db.add_user(u, self.safe_hash(p, salt), salt, True)

    def verify_user(self, u, p):
        """
        Проверка учётных данных пользователя при входе в систему.
        
        Аргументы:
            u (str): Имя пользователя
            p (str): Пароль в открытом виде для проверки
            
        Возвращает:
            bool: True если пароль верный, False в противном случае или если пользователь не найден
            
        Примечание:
            Метод автоматически определяет тип хеширования (безопасный/небезопасный)
            по флагу is_safe в базе данных и использует соответствующий алгоритм проверки.
        """
        try:
            row = self.db.fetch_user(u)
            if not row:
                return False

            h, salt, safe = row

            if int(safe) == 1:
                return bcrypt.checkpw((p + salt).encode(), h.encode())
            else:
                return self.unsafe_hash(p) == h

        except Exception as e:
            print("ERROR:", e)
            return False

    def bruteforce(self, target):
        """
        Демонстрация брутфорс-атаки на SHA-256 хеш (для учебных целей).
        
        Аргументы:
            target (str): SHA-256 хеш, который нужно взломать
            
        Возвращает:
            str или None: Найденный пароль (число в виде строки) или None если не найден
            
        Примечание:
            - Перебираются только числа от 0 до bruteforce_iters-1
            - Используется tqdm для отображения прогресса
            - Создано исключительно для демонстрации уязвимости простых хешей
        """
        for i in tqdm(range(self.settings["bruteforce_iters"])):
            if self.unsafe_hash(str(i)) == target:
                return str(i)
        return None

    def close(self):
        """
        Закрытие соединения с базой данных.
        
        Примечание:
            В текущей реализации не требуется, так как соединения создаются
            каждый раз заново, но метод оставлен для совместимости и
            возможного будущего использования пула соединений.
        """
        pass