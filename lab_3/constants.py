RSA_PRIVATE_FILE = "rsa_private.pem"           # Закрытый ключ RSA
RSA_PUBLIC_FILE = "rsa_public.pem"             # Открытый ключ RSA
CAST5_KEY_FILE = "cast5_key.bin"               # Симметричный ключ CAST-5
ENCRYPTED_CAST5_KEY_FILE = "encrypted_cast5_key.bin"  # CAST-5 ключ, зашифрованный RSA

KEY_FILES = [RSA_PRIVATE_FILE, RSA_PUBLIC_FILE, CAST5_KEY_FILE, ENCRYPTED_CAST5_KEY_FILE]

CAST5_MIN_KEY_LEN = 40      # Минимальная длина ключа CAST-5 (бит)
CAST5_MAX_KEY_LEN = 128     # Максимальная длина ключа CAST-5 (бит)
CAST5_KEY_STEP = 8          # Шаг изменения длины ключа (бит)
CAST5_DEFAULT_KEY_LEN = 128 # Длина ключа по умолчанию

RSA_KEY_SIZE = 2048         # Размер RSA ключа (бит)