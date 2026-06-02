"""
Пользовательские исключения системы.
"""


class CryptoSystemError(Exception):
    """Базовое исключение криптографической системы."""
    pass


class FileProcessingError(CryptoSystemError):
    """Ошибка обработки файла."""
    pass


class KeyGenerationError(CryptoSystemError):
    """Ошибка генерации ключей."""
    pass


class EncryptionError(CryptoSystemError):
    """Ошибка шифрования."""
    pass


class DecryptionError(CryptoSystemError):
    """Ошибка дешифрования."""
    pass


class KeyLoadError(CryptoSystemError):
    """Ошибка загрузки ключа."""
    pass
