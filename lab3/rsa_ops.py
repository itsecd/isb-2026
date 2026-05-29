from cryptography.hazmat.primitives import (
    hashes,
    serialization
)
from cryptography.hazmat.primitives.asymmetric import (
    rsa,
    padding as asym_padding
)

from exceptions import (
    KeyGenerationError,
    KeyLoadError,
    EncryptionError,
    DecryptionError,
    FileProcessingError
)

from file_utils import (
    read_bytes,
    write_bytes
)


def generate_rsa_keys(
        public_exponent: int,
        key_size: int
):
    """
    Генерирует пару RSA ключей.

    :param public_exponent:
        Публичная экспонента RSA.
    :param key_size:
        Размер ключа RSA.
    :return:
        Кортеж из private_key
        и public_key.
    :raises KeyGenerationError:
        При ошибке генерации.
    """
    try:
        private_key = (
            rsa.generate_private_key(
                public_exponent=(
                    public_exponent
                ),
                key_size=key_size
            )
        )

        return (
            private_key,
            private_key.public_key()
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
    Сохраняет private key.

    :param private_key:
        Приватный RSA ключ.
    :param path:
        Путь сохранения.
    :raises FileProcessingError:
        При ошибке записи.
    """
    try:
        private_key_bytes = (
            private_key.private_bytes(
                encoding=(
                    serialization
                    .Encoding
                    .PEM
                ),
                format=(
                    serialization
                    .PrivateFormat
                    .TraditionalOpenSSL
                ),
                encryption_algorithm=(
                    serialization
                    .NoEncryption()
                )
            )
        )

        write_bytes(
            path,
            private_key_bytes
        )

    except Exception as error:
        raise FileProcessingError(
            f"Ошибка сохранения "
            f"private key: {error}"
        ) from error


def save_public_key(
        public_key,
        path: str
) -> None:
    """
    Сохраняет public key.

    :param public_key:
        Публичный RSA ключ.
    :param path:
        Путь сохранения.
    :raises FileProcessingError:
        При ошибке записи.
    """
    try:
        public_key_bytes = (
            public_key.public_bytes(
                encoding=(
                    serialization
                    .Encoding
                    .PEM
                ),
                format=(
                    serialization
                    .PublicFormat
                    .SubjectPublicKeyInfo
                )
            )
        )

        write_bytes(
            path,
            public_key_bytes
        )

    except Exception as error:
        raise FileProcessingError(
            f"Ошибка сохранения "
            f"public key: {error}"
        ) from error


def load_private_key(
        path: str
):
    """
    Загружает private key.

    :param path:
        Путь к PEM файлу.
    :return:
        Объект private key.
    :raises KeyLoadError:
        При ошибке загрузки.
    """
    try:
        key_data = read_bytes(path)

        return (
            serialization
            .load_pem_private_key(
                key_data,
                password=None
            )
        )

    except Exception as error:
        raise KeyLoadError(
            f"Ошибка загрузки "
            f"private key: {error}"
        ) from error


def load_public_key(
        path: str
):
    """
    Загружает public key.

    :param path:
        Путь к PEM файлу.
    :return:
        Объект public key.
    :raises KeyLoadError:
        При ошибке загрузки.
    """
    try:
        key_data = read_bytes(path)

        return (
            serialization
            .load_pem_public_key(
                key_data
            )
        )

    except Exception as error:
        raise KeyLoadError(
            f"Ошибка загрузки "
            f"public key: {error}"
        ) from error


def encrypt_symmetric_key(
        key: bytes,
        public_key
) -> bytes:
    """
    Шифрует симметричный ключ.

    :param key:
        Симметричный ключ.
    :param public_key:
        Публичный RSA ключ.
    :return:
        Зашифрованный ключ.
    :raises EncryptionError:
        При ошибке шифрования.
    """
    try:
        return public_key.encrypt(
            key,
            asym_padding.OAEP(
                mgf=(
                    asym_padding.MGF1(
                        algorithm=(
                            hashes.SHA256()
                        )
                    )
                ),
                algorithm=(
                    hashes.SHA256()
                ),
                label=None
            )
        )

    except Exception as error:
        raise EncryptionError(
            f"Ошибка шифрования "
            f"ключа: {error}"
        ) from error


def decrypt_symmetric_key(
        encrypted_key: bytes,
        private_key
) -> bytes:
    """
    Расшифровывает ключ.

    :param encrypted_key:
        Зашифрованный ключ.
    :param private_key:
        Приватный RSA ключ.
    :return:
        Расшифрованный ключ.
    :raises DecryptionError:
        При ошибке дешифрования.
    """
    try:
        return private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=(
                    asym_padding.MGF1(
                        algorithm=(
                            hashes.SHA256()
                        )
                    )
                ),
                algorithm=(
                    hashes.SHA256()
                ),
                label=None
            )
        )

    except Exception as error:
        raise DecryptionError(
            f"Ошибка дешифрования "
            f"ключа: {error}"
        ) from error
