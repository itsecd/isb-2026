class HybridCryptoError(Exception):
    """Базовое исключение для всей гибридной криптосистемы."""
    pass

class SymmetricCryptoError(HybridCryptoError):
    """Исключение для ошибок при работе с симметричным шифрованием (AES)."""
    pass

class AsymmetricCryptoError(HybridCryptoError):
    """Исключение для ошибок при работе с асимметричным шифрованием (RSA)."""
    pass