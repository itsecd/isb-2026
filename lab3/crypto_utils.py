import os

from cryptography.hazmat.primitives import (
    padding,
    hashes,
    serialization
)

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

from cryptography.hazmat.primitives.asymmetric import (
    rsa,
    padding as asym_padding
)

from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key
)

from constants import *

from exceptions import (
    KeyGenerationError,
    EncryptionError,
    DecryptionError,
    KeyLoadError,
    FileProcessingError
)


def generate_cast5_key(
        key_size_bits: int
) -> bytes:
    """
    Генерирует ключ CAST5.

    Args:
        key_size_bits (int):
            Размер ключа в битах.

    Returns:
        bytes:
            Сгенерированный ключ.

    Raises:
        KeyGenerationError:
            Если размер ключа некорректен.
    """

    try:
        match (
            CAST5_MIN_KEY_SIZE
            <= key_size_bits
            <= CAST5_MAX_KEY_SIZE,

            key_size_bits
            % CAST5_KEY_STEP
        ):
            case (True, 0):
                pass

            case _:
                raise ValueError(
                    "Некорректный "
                    "размер ключа "
                    "CAST5"
                )
        return os.urandom(
            key_size_bits // 8
        )

    except Exception as error:
        raise KeyGenerationError(
            f"Ошибка генерации "
            f"ключа: {error}"
        ) from error


def encrypt_file_cast5(
        input_path: str,
        output_path: str,
        key: bytes
) -> None:
    """
    Шифрует файл алгоритмом CAST5.

    Args:
        input_path (str):
            Путь к исходному файлу.

        output_path (str):
            Путь сохранения
            зашифрованного файла.

        key (bytes):
            Симметричный ключ.

    Raises:
        EncryptionError:
            Если шифрование
            завершилось ошибкой.
    """

    try:
        with open(
                input_path,
                "rb"
        ) as file:
            data = file.read()

        padder = (
            padding.PKCS7(
                CAST5_BLOCK_SIZE
            ).padder()
        )

        padded_data = (
            padder.update(data)
            + padder.finalize()
        )

        iv = os.urandom(
            CAST5_IV_SIZE
        )

        cipher = Cipher(
            algorithms.CAST5(key),
            modes.CBC(iv)
        )

        encryptor = (
            cipher.encryptor()
        )

        encrypted_data = (
            encryptor.update(
                padded_data
            )
            + encryptor.finalize()
        )

        with open(
                output_path,
                "wb"
        ) as file:
            file.write(iv)
            file.write(
                encrypted_data
            )

    except Exception as error:
        raise EncryptionError(
            f"Ошибка шифрования "
            f"файла: {error}"
        ) from error


def decrypt_file_cast5(
        input_path: str,
        output_path: str,
        key: bytes
) -> None:
    """
    Дешифрует файл алгоритмом CAST5.

    Args:
        input_path (str):
            Путь к зашифрованному
            файлу.

        output_path (str):
            Путь сохранения
            расшифрованного файла.

        key (bytes):
            Симметричный ключ.

    Raises:
        DecryptionError:
            Если дешифрование
            завершилось ошибкой.
    """

    try:
        with open(
                input_path,
                "rb"
        ) as file:
            content = (
                file.read()
            )

        iv = content[
             :CAST5_IV_SIZE
        ]

        encrypted_data = (
            content[
                CAST5_IV_SIZE:
            ]
        )

        cipher = Cipher(
            algorithms.CAST5(
                key
            ),
            modes.CBC(iv)
        )

        decryptor = (
            cipher.decryptor()
        )

        decrypted_padded = (
            decryptor.update(
                encrypted_data
            )
            + decryptor.finalize()
        )

        unpadder = (
            padding.PKCS7(
                CAST5_BLOCK_SIZE
            ).unpadder()
        )

        decrypted_data = (
            unpadder.update(
                decrypted_padded
            )
            + unpadder.finalize()
        )

        with open(
                output_path,
                "wb"
        ) as file:
            file.write(
                decrypted_data
            )

    except Exception as error:
        raise DecryptionError(
            f"Ошибка "
            f"дешифрования: "
            f"{error}"
        ) from error


def generate_rsa_keys():
    """
    Генерирует пару RSA ключей.

    Returns:
        tuple:
            Private и public key.

    Raises:
        KeyGenerationError:
            Если генерация
            завершилась ошибкой.
    """

    try:
        private_key = (
            rsa.generate_private_key(
                public_exponent=
                RSA_PUBLIC_EXPONENT,
                key_size=
                RSA_KEY_SIZE
            )
        )

        public_key = (
            private_key.public_key()
        )

        return (
            private_key,
            public_key
        )

    except Exception as error:
        raise KeyGenerationError(
            f"Ошибка генерации "
            f"RSA: {error}"
        ) from error


def save_private_key(
        private_key,
        path: str
) -> None:
    """
    Сохраняет приватный ключ.

    Args:
        private_key:
            RSA private key.

        path (str):
            Путь сохранения.
    """

    try:
        with open(
                path,
                "wb"
        ) as file:
            file.write(
                private_key.private_bytes(
                    encoding=
                    serialization
                    .Encoding.PEM,

                    format=
                    serialization
                    .PrivateFormat
                    .TraditionalOpenSSL,

                    encryption_algorithm=
                    serialization
                    .NoEncryption()
                )
            )

    except Exception as error:
        raise FileProcessingError(
            f"Ошибка сохранения "
            f"private key: "
            f"{error}"
        ) from error


def save_public_key(
        public_key,
        path: str
) -> None:
    """
    Сохраняет публичный ключ.

    Args:
        public_key:
            RSA public key.

        path (str):
            Путь сохранения.
    """

    try:
        with open(
                path,
                "wb"
        ) as file:
            file.write(
                public_key.public_bytes(
                    encoding=
                    serialization
                    .Encoding.PEM,

                    format=
                    serialization
                    .PublicFormat
                    .SubjectPublicKeyInfo
                )
            )

    except Exception as error:
        raise FileProcessingError(
            f"Ошибка сохранения "
            f"public key: "
            f"{error}"
        ) from error


def load_private_key(
        path: str
):
    """
    Загружает private key.

    Args:
        path (str):
            Путь к ключу.

    Returns:
        RSAPrivateKey
    """

    try:
        with open(
                path,
                "rb"
        ) as file:
            return (
                load_pem_private_key(
                    file.read(),
                    password=None
                )
            )

    except Exception as error:
        raise KeyLoadError(
            f"Ошибка загрузки "
            f"private key: "
            f"{error}"
        ) from error


def load_public_key(
        path: str
):
    """
    Загружает public key.

    Args:
        path (str):
            Путь к ключу.

    Returns:
        RSAPublicKey
    """

    try:
        with open(
                path,
                "rb"
        ) as file:
            return (
                load_pem_public_key(
                    file.read()
                )
            )

    except Exception as error:
        raise KeyLoadError(
            f"Ошибка загрузки "
            f"public key: "
            f"{error}"
        ) from error


def encrypt_symmetric_key(
        key: bytes,
        public_key
) -> bytes:
    """
    Шифрует симметричный ключ RSA.

    Args:
        key (bytes):
            Симметричный ключ.

        public_key:
            RSA public key.

    Returns:
        bytes:
            Зашифрованный ключ.
    """

    try:
        return public_key.encrypt(
            key,

            asym_padding.OAEP(
                mgf=
                asym_padding.MGF1(
                    algorithm=
                    hashes.SHA256()
                ),

                algorithm=
                hashes.SHA256(),

                label=None
            )
        )

    except Exception as error:
        raise EncryptionError(
            f"Ошибка "
            f"шифрования ключа: "
            f"{error}"
        ) from error


def decrypt_symmetric_key(
        encrypted_key: bytes,
        private_key
) -> bytes:
    """
    Расшифровывает
    симметричный ключ.

    Args:
        encrypted_key (bytes):
            Зашифрованный ключ.

        private_key:
            RSA private key.

    Returns:
        bytes:
            Расшифрованный ключ.
    """

    try:
        return (
            private_key.decrypt(
                encrypted_key,

                asym_padding.OAEP(
                    mgf=
                    asym_padding.MGF1(
                        algorithm=
                        hashes.SHA256()
                    ),

                    algorithm=
                    hashes.SHA256(),

                    label=None
                )
            )
        )

    except Exception as error:
        raise DecryptionError(
            f"Ошибка "
            f"дешифрования "
            f"ключа: {error}"
        ) from error
