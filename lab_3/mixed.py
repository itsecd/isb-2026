from blowfish import generate_blowfish_key
from rsa import generate_key_pair, encrypt_rsa, load_private_key, decrypt_rsa, save_public_key, save_private_key
from blowfish import encrypt_blowfish
from fileutils import write_bytes, read_bytes


def generate_keys(settings: dict) -> None:
    """
    Generate RSA and Blowfish keys.
    :param settings: json-settings
    """
    key_length = settings['symmetric_key_length']
    print(f"Генерация Blowfish ключа длиной {key_length} бит")
    symmetric_key = generate_blowfish_key(key_length)

    print("Генерация пары ключей RSA длиной 2048 бит")
    private_key, public_key = generate_key_pair()

    save_private_key(settings['secret_key'], private_key)
    save_public_key(settings['public_key'], public_key)

    encrypted_symmetric_key = encrypt_rsa(public_key, symmetric_key)
    write_bytes(settings['symmetric_key'], encrypted_symmetric_key)

    print("Ключи были сгенерированы и сохранены в файлы")

def get_symmetric_key(settings: dict) -> bytes:
    """
    Help function to decrypt and pass symmetric key.
    :param settings: json-settings
    :return: symmetric key
    """
    private_key = load_private_key(settings['secret_key'])
    encrypted_symmetric_key = read_bytes(settings['symmetric_key'])
    return decrypt_rsa(private_key, encrypted_symmetric_key)


def encrypt_data(settings: dict) -> None:
    """
    Load, encrypt with Blowfish and save data.
    :param settings: json-settings
    """
    print("Чтение ключей и исходного файла")
    symmetric_key = get_symmetric_key(settings)
    data = read_bytes(settings['initial_file'])
    encrypted_data = encrypt_blowfish(symmetric_key, data)
    write_bytes(settings['encrypted_file'], encrypted_data)
    print(f"Текст был зашифрован и записан в {settings['encrypted_file']}")


def decrypt_data(settings: dict) -> None:
    """
    Load, dencrypt with Blowfish and save data.
    :param settings: json-settings
    """
    print("Чтение ключей и зашифрованного файла")
    symmetric_key = get_symmetric_key(settings)
    data = read_bytes(settings['encrypted_file'])
    decrypted_data = encrypt_blowfish(symmetric_key, data)
    write_bytes(settings['decrypted_file'], decrypted_data)
    print(f"Текст был расшифрован и записан в {settings['decrypted_file']}")