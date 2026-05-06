import json

# Размеры ключей
SYMMETRIC_KEY_SIZE = 32          # 256 бит для ChaCha20
NONCE_SIZE = 16                  # 128 бит для ChaCha20
RSA_KEY_SIZE = 2048              # 2048 бит для RSA
RSA_PUBLIC_EXPONENT = 65537      # экспонента для RSA

# Пути к файлам
DEFAULT_SETTINGS_FILE = "settings.json"#для удобства все настройки в одном месте

# Стандартные пути 
DEFAULT_INITIAL_FILE = "initial_file.txt"
DEFAULT_ENCRYPTED_FILE = "encrypted.bin"#зашифрованный файл
DEFAULT_DECRYPTED_FILE = "decrypted.txt"
DEFAULT_SYMMETRIC_KEY_FILE = "symmetric_key.bin"
DEFAULT_NONCE_FILE = "nonce.bin"         
DEFAULT_ENCRYPTED_SYMMETRIC_KEY_FILE = "encrypted_symmetric_key.bin"
DEFAULT_PUBLIC_KEY_FILE = "public_key.pem"
DEFAULT_PRIVATE_KEY_FILE = "private_key.pem"

# Словарь с настройками по умолчанию(используется, если файл settings.json не найден или повреждён)
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

# Загрузка настроек из JSON 
_SETTINGS_LOADED = False

def load_settings_once(settings_file: str = DEFAULT_SETTINGS_FILE) -> dict:
    """Загружает настройки из JSON-файла один раз при запуске программы"""
    global _SETTINGS_LOADED, SETTINGS
    if not _SETTINGS_LOADED:
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                SETTINGS = json.load(f)
            _SETTINGS_LOADED = True
        except FileNotFoundError:
            SETTINGS = DEFAULT_SETTINGS.copy()
            _SETTINGS_LOADED = True
        except json.JSONDecodeError:
            SETTINGS = DEFAULT_SETTINGS.copy()
            _SETTINGS_LOADED = True
    return SETTINGS

# Инициализация настроек (точка входа)
SETTINGS = load_settings_once()