"""
Модуль работы с файлами.
"""

from pathlib import Path


class FileManager:
    """Чтение и запись файлов."""

    @staticmethod
    def read(path: str) -> bytes:
        """Чтение файла."""
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")

        try:
            with open(file_path, "rb") as file:
                return file.read()
        except Exception as exc:
            raise RuntimeError(f"Ошибка чтения файла: {exc}") from exc

    @staticmethod
    def write(path: str, data: bytes) -> None:
        """Запись файла."""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)

            with open(path, "wb") as file:
                file.write(data)

        except Exception as exc:
            raise RuntimeError(f"Ошибка записи файла: {exc}") from exc