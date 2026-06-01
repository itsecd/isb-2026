from UserStorage import UserStorage, StorageError
import hasher

class UserManagerError(Exception):
    """Класс ошибок"""
    pass

class UserManager:
    def __init__(self, storage=None, default_algo="bcrypt"):
        self.storage = storage or UserStorage()
        self.default_algo = default_algo

    def register(self, login, password, algo=None):
        """
        Принимает: Объект класса, логин, пароль и алгоритм
        Возвращает: Ничего (регистрирует пользователя)
        """
        if not isinstance(login, str) or not login.strip():
            raise UserManagerError("Логин не может быть пустым.")
        if not password:
            raise UserManagerError("Пароль не может быть пустым.")
        
        chosen_algo = algo or self.default_algo
        try:
            hash_func = hasher.get_hasher(chosen_algo)
            record = hash_func(password)
            self.storage.add(login, record)
            return record
        except (ValueError, StorageError) as exc:
            raise UserManagerError(str(exc)) from exc

    def authenticate(self, login, password) -> bool:
        """
        Авторизует пользователя в системе
        Принимает: Объект класса, логин, пароль
        Возвращает: Статус авторизации
        """
        try:
            record = self.storage.get(login)
            if not record:
                raise UserManagerError("Пользователь не найден.")
            
            return hasher.verify_password(password, record)
        except StorageError as exc:
            raise UserManagerError(str(exc)) from exc