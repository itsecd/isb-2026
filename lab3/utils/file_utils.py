import os
from typing import Dict, Any, Union


class FileManager:
    """Управление файловыми операциями"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        paths = config.get('paths')
        if paths is None:
            raise KeyError("Секция 'paths' не найдена в конфигурации")
        
        self._keys_dir = paths.get('keys_directory')
        if self._keys_dir is None:
            raise KeyError("Параметр 'keys_directory' не найден в секции 'paths'")
        
        if self._keys_dir:
            try:
                os.makedirs(self._keys_dir, exist_ok=True)
            except Exception as e:
                print(f"Предупреждение: не удалось создать директорию {self._keys_dir}: {e}")
        
        self._paths = paths
    
    def read_file(self, filepath: str, binary: bool = False) -> Union[str, bytes]:
        """Чтение файла"""
        if not filepath:
            raise ValueError("Путь к файлу не может быть пустым")
        
        mode = 'rb' if binary else 'r'
        try:
            with open(filepath, mode) as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу: {filepath}")
        except Exception as e:
            raise IOError(f"Ошибка чтения файла {filepath}: {e}")
    
    def write_file(self, filepath: str, data: Union[str, bytes], binary: bool = False) -> None:
        """Запись файла"""
        if not filepath:
            raise ValueError("Путь к файлу не может быть пустым")
        
        if data is None:
            raise ValueError("Нет данных для записи")
        
        directory = os.path.dirname(filepath)
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                raise IOError(f"Не удалось создать директорию {directory}: {e}")
        
        mode = 'wb' if binary else 'w'
        try:
            with open(filepath, mode) as f:
                f.write(data)
        except PermissionError:
            raise PermissionError(f"Нет прав для записи в файл: {filepath}")
        except Exception as e:
            raise IOError(f"Ошибка записи файла {filepath}: {e}")
    
    def file_exists(self, filepath: str) -> bool:
        """Проверка существования файла"""
        if not filepath:
            return False
        return os.path.exists(filepath)
    
    def get_path(self, key: str) -> str:
        """Получение пути из конфига"""
        filename = self._paths.get(key)
        if filename is None:
            raise KeyError(f"Параметр '{key}' не найден в секции 'paths'")
        
        if not filename:
            raise ValueError(f"Путь для ключа '{key}' пуст")
        
        return os.path.join(self._keys_dir, filename)
    
    def delete_file(self, filepath: str) -> None:
        """Удаление файла"""
        if not filepath:
            raise ValueError("Путь к файлу не может быть пустым")
        
        if not self.file_exists(filepath):
            return
        
        try:
            os.remove(filepath)
        except PermissionError:
            raise PermissionError(f"Нет прав пользователя для удаления файла: {filepath}")
        except Exception as e:
            raise IOError(f"Ошибка удаления файла {filepath}: {e}")