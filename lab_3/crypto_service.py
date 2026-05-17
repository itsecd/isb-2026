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

from file_utils import read_file, write_file


def generate_keys_service(
    config: dict,
    manual_key: bytes | None = None,
) -> None:

    sym_key = manual_key or generate_idea_key()

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


def load_sym_key(config: dict) -> bytes:

    private_key = load_private_key(config["private_key"])

    enc_key = read_file(config["symmetric_key"])

    return decrypt_key(
        private_key,
        enc_key,
    )


def encrypt_service(
    config: dict,
    input_path: str,
) -> None:

    sym_key = load_sym_key(config)

    data = read_file(input_path)

    encrypted = encrypt_data(
        sym_key,
        data,
    )

    write_file(
        config["encrypted_file"],
        encrypted,
    )


def decrypt_service(config: dict) -> None:

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
