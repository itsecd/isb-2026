"""
Module with exception hierarchy for hybrid crypto system.

All exceptions inherit from CryptoSystemError base class,
allowing to catch them either individually or in a single block.
"""


class CryptoSystemError(Exception):
    """
    Base exception for all crypto system errors.

    Attributes:
        message (str): Human-readable error description.
    """

    def __init__(self, message: str = "An error occurred in crypto system") -> None:
        """
        Initializes base exception.

        Args:
            message: Error message text.
        """
        self.message = message
        super().__init__(self.message)


class ConfigError(CryptoSystemError):
    """
    Exception raised for configuration errors.

    Indicates that settings.json file is missing, corrupted,
    or missing required keys.
    """

    def __init__(self, message: str = "Configuration error") -> None:
        """
        Initializes configuration exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)


class FileOperationError(CryptoSystemError):
    """
    Exception raised for file I/O errors.

    Indicates that file not found, no read/write permissions,
    or file has invalid format.
    """

    def __init__(self, message: str = "File operation error") -> None:
        """
        Initializes file operation exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)


class KeyGenerationError(CryptoSystemError):
    """
    Exception raised for key generation errors.

    Indicates that symmetric or asymmetric key generation failed.
    """

    def __init__(self, message: str = "Key generation error") -> None:
        """
        Initializes key generation exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)


class EncryptionError(CryptoSystemError):
    """
    Exception raised for encryption errors.

    Indicates that encryption operation failed.
    """

    def __init__(self, message: str = "Encryption error") -> None:
        """
        Initializes encryption exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)


class DecryptionError(CryptoSystemError):
    """
    Exception raised for decryption errors.

    Indicates that decryption operation failed, possibly due to
    invalid key or corrupted data.
    """

    def __init__(self, message: str = "Decryption error") -> None:
        """
        Initializes decryption exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)


class KeyLoadError(CryptoSystemError):
    """
    Exception raised for key loading errors.

    Indicates that key deserialization from file failed,
    possibly due to corrupted file or invalid format.
    """

    def __init__(self, message: str = "Key loading error") -> None:
        """
        Initializes key loading exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)


class KeySizeError(CryptoSystemError):
    """
    Exception raised for key size validation errors.

    Indicates that key size is invalid for the algorithm.
    """

    def __init__(self, message: str = "Key size error") -> None:
        """
        Initializes key size exception.

        Args:
            message: Error message text.
        """
        super().__init__(message)
