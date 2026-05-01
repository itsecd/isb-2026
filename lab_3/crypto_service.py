from RSA import (
    deserialize_private_rsa_key,
    deserialize_public_rsa_key,
    decrypt_with_rsa_key,
    generate_rsa_keys,
    serialize_private_rsa_key,
    serialize_public_rsa_key,
    encrypt_with_rsa_key,
)

from ChaCha20 import (
    encrypt_with_chacha20_cipher,
    decrypt_with_chacha20_cipher,
    generate_chacha20_key,
    generate_nonce,
)

from functions import (
    deserialize_data,
    serialize_data,
)


def generate_all_keys(
    public_rsa_key_path: str,
    private_rsa_key_path: str,
    symmetric_key_path: str,
    nonce_path: str,
):
    """
    Генерация всех ключей:
    - симметричный ключ
    - одноразовый код nonce
    - пара ключей rsa
    """
    sym_key = generate_chacha20_key()
    nonce = generate_nonce()

    serialize_data(symmetric_key_path, sym_key)
    serialize_data(nonce_path, nonce)

    private_key, public_key = generate_rsa_keys()

    serialize_private_rsa_key(private_key, private_rsa_key_path)
    serialize_public_rsa_key(public_key, public_rsa_key_path)


def encrypt_file(settings: dict):
    """
    Шифрование файла с использованием гибридной криптосистемы.
    """
    public_key = deserialize_public_rsa_key(settings["public_key"])

    sym_key = deserialize_data(settings["symmetric_key"])

    enc_key = encrypt_with_rsa_key(sym_key, public_key)
    serialize_data(settings["encrypted_symmetric_key"], enc_key)

    nonce = deserialize_data(settings["nonce"])
    data = deserialize_data(settings["initial_file"])

    encrypted = encrypt_with_chacha20_cipher(data, sym_key, nonce)

    serialize_data(settings["encrypted_file"], encrypted)


def decrypt_file(settings: dict):
    """
    Расшифровка файла с использованием гибридной криптосистемы.
    """
    private_key = deserialize_private_rsa_key(settings["secret_key"])

    enc_key = deserialize_data(settings["encrypted_symmetric_key"])
    sym_key = decrypt_with_rsa_key(enc_key, private_key)

    nonce = deserialize_data(settings["nonce"])
    data = deserialize_data(settings["encrypted_file"])

    decrypted = decrypt_with_chacha20_cipher(data, sym_key, nonce)

    serialize_data(settings["decrypted_file"], decrypted)