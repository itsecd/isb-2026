"""Константы для гибридной криптосистемы (RSA + ChaCha20)"""

# Размеры ключей
SYMMETRIC_KEY_SIZE = 32          # 256 бит для ChaCha20
NONCE_SIZE = 16                  # 128 бит для ChaCha20
RSA_KEY_SIZE = 2048              # 2048 бит для RSA(минимальны размер обеспечивающий безопасное)
RSA_PUBLIC_EXPONENT = 65537

# Пути к файлам
DEFAULT_SETTINGS_FILE = "settings.json"

# Стандартные пути (будут перезаписаны из settings.json)
DEFAULT_INITIAL_FILE = "initial_file.txt"
DEFAULT_ENCRYPTED_FILE = "encrypted.bin"
DEFAULT_DECRYPTED_FILE = "decrypted.txt"
DEFAULT_SYMMETRIC_KEY_FILE = "symmetric_key.bin"
DEFAULT_NONCE_FILE = "nonce.bin"          # для хранения nonce отдельно
DEFAULT_ENCRYPTED_SYMMETRIC_KEY_FILE = "encrypted_symmetric_key.bin"
DEFAULT_PUBLIC_KEY_FILE = "public_key.pem"
DEFAULT_PRIVATE_KEY_FILE = "private_key.pem"

# Режимы работы
MODE_GENERATION = "generation"
MODE_ENCRYPTION = "encryption"
MODE_DECRYPTION = "decryption"

# Словарь с настройками по умолчанию
DEFAULT_SETTINGS = {
    "initial_file": DEFAULT_INITIAL_FILE,
    "encrypted_file": DEFAULT_ENCRYPTED_FILE,
    "decrypted_file": DEFAULT_DECRYPTED_FILE,
    "symmetric_key_file": DEFAULT_SYMMETRIC_KEY_FILE,
    "nonce_file": DEFAULT_NONCE_FILE,
    "encrypted_symmetric_key_file": DEFAULT_ENCRYPTED_SYMMETRIC_KEY_FILE,
    "public_key_file": DEFAULT_PUBLIC_KEY_FILE,
    "private_key_file": DEFAULT_PRIVATE_KEY_FILE
}