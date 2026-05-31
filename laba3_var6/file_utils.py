from exceptions import FileOperationError


class FileWorker:
    @staticmethod
    def read_binary(filepath: str) -> bytes:
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            print(f"  [OK] Прочитан бинарный файл: {filepath}")
            return content
        except FileNotFoundError:
            raise FileOperationError(f"Файл '{filepath}' не существует")
        except PermissionError:
            raise FileOperationError(f"Нет доступа для чтения: {filepath}")

    @staticmethod
    def read_text(filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"  [OK] Прочитан текстовый файл: {filepath}")
            return text
        except FileNotFoundError:
            raise FileOperationError(f"Файл '{filepath}' не найден")
        except UnicodeDecodeError:
            raise FileOperationError(f"Ошибка кодировки в файле: {filepath}")

    @staticmethod
    def write_binary(filepath: str, data: bytes):
        try:
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"  [OK] Сохранён бинарный файл: {filepath}")
        except PermissionError:
            raise FileOperationError(f"Нет прав на запись: {filepath}")

    @staticmethod
    def write_text(filepath: str, content: str):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Сохранён текстовый файл: {filepath}")
        except PermissionError:
            raise FileOperationError(f"Нет прав на запись: {filepath}")