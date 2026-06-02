"""
Custom exceptions for the hybrid crypto system.

Provides specific exception types for different failure scenarios,
allowing fine-grained error handling throughout the application.
"""


class CryptoError(Exception):
    """Base exception for all crypto system errors."""
    pass


class KeyGenerationError(CryptoError):
    """Raised when cryptographic key generation fails."""
    pass


class KeyLoadError(CryptoError):
    """Raised when loading a key from a file fails."""
    pass


class EncryptionError(CryptoError):
    """Raised when encryption operation fails."""
    pass


class DecryptionError(CryptoError):
    """Raised when decryption operation fails."""
    pass


class FileOperationError(CryptoError):
    """Raised when file read/write operations fail."""
    pass


class PaddingError(CryptoError):
    """Raised when padding or unpadding fails."""
    pass