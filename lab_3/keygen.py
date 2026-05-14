from blowfish import generate_blowfish_key
from rsa import generate_key_pair, save_public_key, save_private_key, encrypt_rsa
from fileutils import write_bytes


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
