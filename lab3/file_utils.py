"""
Модуль для безопасной работы с файловой системой.

Предоставляет функции чтения и записи файлов
с единообразной обработкой ошибок.
"""

from exceptions import FileOperationError


class FileHandler:
    """
    Класс-утилита для файловых операций.

    Все методы являются статическими, так как класс не хранит состояние.
    Предоставляет единый интерфейс для чтения и записи текстовых
     и бинарных файлов.
    """

    @staticmethod
    def read_bytes(file_path: str) -> bytes:
        """
        Читает содержимое бинарного файла.

        Аргументы:
            file_path: Путь к файлу.

        Возвращает:
            bytes: Содержимое файла в байтах.

        Исключения:
            FileOperationError: Если файл не найден или нет прав на чтение.
        """
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            print(f"Прочитан файл: {file_path}")
            return content
        except FileNotFoundError:
            raise FileOperationError(
                f"Файл '{file_path}' не найден. "
                f"Проверьте правильность пути в settings.json."
            )
        except PermissionError:
            raise FileOperationError(
                f"Нет прав на чтение файла '{file_path}'."
            )

    @staticmethod
    def read_text(file_path: str) -> str:
        """
        Читает содержимое текстового файла в кодировке UTF-8.

        Аргументы:
            file_path: Путь к файлу.

        Возвращает:
            str: Содержимое файла как строка.

        Исключения:
            FileOperationError: Если файл не найден,
             нет прав или неверная кодировка.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print(f"Прочитан файл: {file_path}")
            return content
        except FileNotFoundError:
            raise FileOperationError(
                f"Файл '{file_path}' не найден. "
                f"Проверьте правильность пути в settings.json."
            )
        except PermissionError:
            raise FileOperationError(
                f"Нет прав на чтение файла '{file_path}'."
            )
        except UnicodeDecodeError:
            raise FileOperationError(
                f"Файл '{file_path}' не является текстовым в кодировке UTF-8."
            )

    @staticmethod
    def write_bytes(file_path: str, data: bytes) -> None:
        """
        Записывает бинарные данные в файл.

        Аргументы:
            file_path: Путь к файлу.
            data: Данные для записи.

        Исключения:
            FileOperationError: Если нет прав на запись.
        """
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
            print(f"Данные записаны в: {file_path}")
        except PermissionError:
            raise FileOperationError(
                f"Нет прав на запись в файл '{file_path}'."
            )

    @staticmethod
    def write_text(file_path: str, content: str) -> None:
        """
        Записывает текст в файл в кодировке UTF-8.

        Аргументы:
            file_path: Путь к файлу.
            content: Текст для записи.

        Исключения:
            FileOperationError: Если нет прав на запись.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Текст записан в: {file_path}")
        except PermissionError:
            raise FileOperationError(
                f"Нет прав на запись в файл '{file_path}'."
            )