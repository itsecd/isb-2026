from crypto_asymmetric import load_private_key, decrypt_rsa, encrypt_rsa, save_public_key, save_private_key, generate_key_pair
from crypto_symmetric import encrypt_blowfish, decrypt_blowfish, generate_blowfish_key, validate_blowfish_key_length
from utils import write_bytes, read_bytes


def get_symmetric_key(settings: dict) -> bytes:
    """
    Извлекает и расшифровывает симметричный ключ Blowfish с помощью RSA приватного ключа.
    
    Args:
        settings: Словарь с настройками, содержащий пути к ключам
    
    Returns:
        bytes: Расшифрованный симметричный ключ Blowfish
    """
    private_key = load_private_key(settings['secret_key'])
    encrypted_symmetric_key = read_bytes(settings['symmetric_key'])
    return decrypt_rsa(private_key, encrypted_symmetric_key)


def generate_hybrid_keys(settings: dict) -> None:
    """
    Генерирует полный набор ключей для гибридной криптосистемы.
    
    Args:
        settings: Словарь с настройками, содержащий пути для сохранения ключей
    """
    key_length = settings['symmetric_key_length']
    validate_blowfish_key_length(key_length)
    
    print(f"Генерация Blowfish ключа длиной {key_length} бит")
    symmetric_key = generate_blowfish_key(key_length)
    
    print("Генерация пары ключей RSA длиной 2048 бит")
    private_key, public_key = generate_key_pair()
    
    save_private_key(settings['secret_key'], private_key)
    save_public_key(settings['public_key'], public_key)
    
    encrypted_symmetric_key = encrypt_rsa(public_key, symmetric_key)
    write_bytes(settings['symmetric_key'], encrypted_symmetric_key)
    
    print("Ключи были сгенерированы и сохранены в файлы")


def encrypt_data(settings: dict) -> None:
    """
    Выполняет гибридное шифрование файла.
    
    Args:
        settings: Словарь с настройками, содержащий пути к файлам
    """
    print("Чтение ключей и исходного файла")
    symmetric_key = get_symmetric_key(settings)
    data = read_bytes(settings['initial_file'])
    encrypted_data = encrypt_blowfish(symmetric_key, data)
    write_bytes(settings['encrypted_file'], encrypted_data)
    print(f"Текст был зашифрован и записан в {settings['encrypted_file']}")


def decrypt_data(settings: dict) -> None:
    """
    Выполняет гибридное дешифрование файла.
    
    Args:
        settings: Словарь с настройками, содержащий пути к файлам
    """
    print("Чтение ключей и зашифрованного файла")
    symmetric_key = get_symmetric_key(settings)
    data = read_bytes(settings['encrypted_file'])
    decrypted_data = decrypt_blowfish(symmetric_key, data)
    write_bytes(settings['decrypted_file'], decrypted_data)
    print(f"Текст был расшифрован и записан в {settings['decrypted_file']}")
