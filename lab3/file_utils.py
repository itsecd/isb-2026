import json
from pathlib import Path


class FileService:
    """Класс для выполнения безопасных операций ввода-вывода и работы с конфигурацией."""

    def load_settings(self, path: str) -> dict:
        """Загружает настройки приложения из файла JSON.

        Args:
            path (str): Путь к файлу конфигурации JSON.

        Returns:
            dict: Словарь с загруженными параметрами конфигурации.

        Raises:
            ValueError: Если файл содержит некорректный JSON или структуру.
        """
        settings_path = Path(path)
        try:
            with settings_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as exc:
            raise ValueError(f"Файл настроек не найден: {settings_path}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Ошибка в структуре JSON-файла: {settings_path}") from exc
        except OSError as exc:
            raise ValueError(f"Не удалось прочитать файл настроек: {settings_path}") from exc

    def read_bytes(self, path: str) -> bytes:
        """Считывает содержимое файла в виде байтовой строки.

        Args:
            path (str): Путь к читаемому файлу.

        Returns:
            bytes: Байтовое содержимое файла.

        Raises:
            ValueError: При невозможности найти или прочитать файл.
        """
        file_path = Path(path)
        try:
            with file_path.open("rb") as file:
                return file.read()
        except FileNotFoundError as exc:
            raise ValueError(f"Файл не найден: {file_path}") from exc
        except OSError as exc:
            raise ValueError(f"Ошибка чтения файла: {file_path}") from exc

    def write_bytes(self, path: str, data: bytes) -> None:
        """Записывает байты в файл и автоматически создает родительские директории.

        Args:
            path (str): Путь к целевому файлу для записи.
            data (bytes): Байты данных для записи.

        Raises:
            ValueError: При ошибках записи данных или создании папок.
        """
        file_path = Path(path)
        try:
            self._create_parent_folder(file_path)
            with file_path.open("wb") as file:
                file.write(data)
        except OSError as exc:
            raise ValueError(f"Ошибка записи файла: {file_path}") from exc

    def _create_parent_folder(self, path: Path) -> None:
        """Создает родительскую папку для указанного пути, если она не существует.

        Args:
            path (Path): Объект Path целевого файла.

        Raises:
            OSError: Если не удалось создать директорию.
        """
        folder = path.parent
        match str(folder):
            case ".":
                return
            case _:
                folder.mkdir(parents=True, exist_ok=True)