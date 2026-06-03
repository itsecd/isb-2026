import json
from pathlib import Path
from typing import Dict, Any


class FileService:
    """Класс для выполнения безопасных операций ввода-вывода и работы с конфигурацией.
    
    Предоставляет методы для чтения и записи файлов с обработкой исключений
    и созданием необходимых директорий.
    """
    
    def load_settings(self, path: str) -> Dict[str, Any]:
        """Загружает настройки приложения из JSON-файла.
        
        Args:
            path (str): Путь к JSON-файлу с настройками.
            
        Returns:
            Dict[str, Any]: Словарь с загруженными настройками.
            
        Raises:
            ValueError: Если файл не найден, имеет неверный формат JSON
                       или возникла ошибка чтения.
                       
        Example:
            >>> service = FileService()
            >>> settings = service.load_settings("config/settings.json")
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
        """Читает бинарные данные из файла.
        
        Args:
            path (str): Путь к файлу для чтения.
            
        Returns:
            bytes: Содержимое файла в виде байтовой строки.
            
        Raises:
            ValueError: Если файл не найден или возникла ошибка чтения.
            
        Example:
            >>> service = FileService()
            >>> data = service.read_bytes("document.pdf")
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
        """Записывает бинарные данные в файл.
        
        Автоматически создает родительские директории, если они не существуют.
        
        Args:
            path (str): Путь для сохранения файла.
            data (bytes): Бинарные данные для записи.
            
        Raises:
            ValueError: Если возникла ошибка записи в файл.
            
        Example:
            >>> service = FileService()
            >>> service.write_bytes("output/encrypted.bin", encrypted_data)
        """
        file_path = Path(path)
        try:
            self._create_parent_folder(file_path)
            with file_path.open("wb") as file:
                file.write(data)
        except OSError as exc:
            raise ValueError(f"Ошибка записи файла: {file_path}") from exc
    
    def _create_parent_folder(self, path: Path) -> None:
        """Создает родительские директории для указанного пути.
        
        Args:
            path (Path): Объект Path, для которого нужно создать родительские папки.
            
        Note:
            Метод игнорирует создание папок для корневого пути (".").
            Использует exist_ok=True, чтобы не вызывать ошибку, если папка уже существует.
            
        Example:
            >>> service = FileService()
            >>> service._create_parent_folder(Path("deep/nested/folder/file.txt"))
            # Создаст папки "deep/nested/folder/"
        """
        folder = path.parent
        match str(folder):
            case ".":
                return
            case _:
                folder.mkdir(parents=True, exist_ok=True)
