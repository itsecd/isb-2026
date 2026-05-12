
"""
Константы гибридной криптосистемы.
"""

# CAST5
CAST5_BLOCK_SIZE_BITS = 64
CAST5_BLOCK_SIZE_BYTES = 8

# Padding
PADDING_BLOCK_SIZE = 64

# IV
IV_SIZE_BYTES = 8

# Алгоритмы
SYMMETRIC_ALGORITHM = "CAST5"
ASYMMETRIC_ALGORITHM = "RSA"

# Сообщения об ошибках
ERROR_INVALID_KEY_SIZE = "Неверная длина ключа"
ERROR_NO_FILE = "Файл не выбран"
ERROR_EMPTY_PATH = "Путь к файлу не задан"
