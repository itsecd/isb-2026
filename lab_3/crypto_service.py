from crypto.symmetric import (
    generate_idea_key,
    encrypt_data,
    decrypt_data,
)

from crypto.asymmetric import (
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    load_private_key,
    encrypt_key,
    decrypt_key,
)

from file_utils import (
    read_file,
    write_file,
)


def load_sym_key(config: dict) -> bytes:
    """
    Загружает и расшифровывает симметричный ключ.
    """

    private_key = load_private_key(config["private_key"])

    enc_key = read_file(config["symmetric_key"])

    return decrypt_key(
        private_key,
        enc_key,
    )


def generate_keys_service(
    config: dict,
    sym_key: bytes | None = None,
) -> None:
    """
    Генерирует RSA и симметричные ключи.
    """

    if sym_key is None:
        sym_key = generate_idea_key()

    private_key, public_key = generate_rsa_keys()

    save_private_key(
        private_key,
        config["private_key"],
    )

    save_public_key(
        public_key,
        config["public_key"],
    )

    enc_key = encrypt_key(
        public_key,
        sym_key,
    )

    write_file(
        config["symmetric_key"],
        enc_key,
    )


def encrypt_file_service(
    config: dict,
) -> None:
    """
    Шифрует файл.
    """

    sym_key = load_sym_key(config)

    data = read_file(config["initial_file"])

    encrypted = encrypt_data(
        sym_key,
        data,
    )

    write_file(
        config["encrypted_file"],
        encrypted,
    )


def decrypt_file_service(
    config: dict,
) -> None:
    """
    Дешифрует файл.
    """

    sym_key = load_sym_key(config)

    data = read_file(config["encrypted_file"])

    decrypted = decrypt_data(
        sym_key,
        data,
    )

    write_file(
        config["decrypted_file"],
        decrypted,
    )
