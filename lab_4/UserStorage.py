import json
from pathlib import Path

class StorageError(Exception):
    """Ошибки при работе с хранилищем."""
    pass

class UserStorage:
    def __init__(self, path="users.json"):
        self.path = Path(path)

    def _read(self) -> dict:
        """
        Читает Json данные
        Принимает: объект класса UserStorage
        Возвращает: Прочитанный текст
        """
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            raise StorageError("Файл базы данных поврежден.")

    def _write(self, data: dict):
        """
        Прописывает в Json файл
        Принимает: объект класса и данные
        Возвращает: записывает данные в файл
        """
        try:
            self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception as e:
            raise StorageError(f"Не удалось записать данные: {e}")

    def add(self, login: str, record: dict):
        """
        Добавляет данные в файл
        Принимает: Объект класса и данные
        Возвращает: добавляет данные в Json
        """
        data = self._read()
        if login in data:
            raise StorageError(f"Пользователь {login} уже существует.")
        data[login] = record
        self._write(data)

    def get(self, login: str) -> dict:
        """
        Получает логин из Json
        Принимает: Объект класса и запись (логин)
        Возвращает: полученный логин
        """
        return self._read().get(login)