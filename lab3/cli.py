from rsa_utils import (
    generate_rsa_keys,
    encrypt_symmetric_key,
    decrypt_symmetric_key,
)

from cast5_utils import (
    generate_cast5_key,
    encrypt_file,
    decrypt_file,
)


def keygen_mode(args):
    """
    Run CLI key generation mode.

    args:
        args:
            parsed CLI arguments
    """

    generate_rsa_keys(
        args.public_key,
        args.private_key,
    )

    sym_key = generate_cast5_key(
        args.key_size
    )

    encrypt_symmetric_key(
        sym_key,
        args.public_key,
        args.encrypted_key,
    )


def encrypt_mode(args):
    """
    Run CLI encryption mode.

    args:
        args:
            parsed CLI arguments
    """

    sym_key = decrypt_symmetric_key(
        args.private_key,
        args.encrypted_key,
    )

    encrypt_file(
        args.input_file,
        args.output_file,
        sym_key,
    )


def decrypt_mode(args):
    """
    Run CLI decryption mode.

    args:
        args:
            parsed CLI arguments
    """

    sym_key = decrypt_symmetric_key(
        args.private_key,
        args.encrypted_key,
    )

    decrypt_file(
        args.input_file,
        args.output_file,
        sym_key,
    )
