import sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def serialize_asymmetric_keys(
    private_key: rsa.RSAPrivateKey,
    public_key: rsa.RSAPublicKey,
    public_way: str,
    private_way: str,
) -> None:
    """Сохраняет открытый и закрытый ключи в файлы PEM."""
    try:
        with open(public_way, "wb") as public_out:
            public_out.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

        with open(private_way, "wb") as private_out:
            private_out.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    except IOError as e:
        print(f"Ошибка записи файлов ключей: {e}")
        sys.exit(1)


def load_private_key(private_way: str) -> rsa.RSAPrivateKey:
    """Загружает закрытый ключ из файла."""
    try:
        with open(private_way, "rb") as pem_in:
            private_bytes = pem_in.read()
            return load_pem_private_key(private_bytes, password=None)
    except FileNotFoundError:
        print(f"Ошибка: Файл закрытого ключа '{private_way}' не найден!")
        sys.exit(1)


def read_file(path_file: str) -> str:
    """Читает текст из файла."""
    try:
        with open(path_file, "r", encoding="utf-8") as t:
            text = t.read()
            return text
    except FileNotFoundError:
        print(f" Ошибка: Исходный файл '{path_file}' не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка чтения файла '{path_file}': {e}")
        sys.exit(1)


def write_text_file(text: str, file_path: str) -> None:
    """Записывает текст в файл."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
    except IOError as e:
        print(f"Ошибка записи в файл '{file_path}': {e}")
        sys.exit(1)


def save_symmetric_key(encrypted_key: bytes, output_path: str) -> None:
    """Сохраняет зашифрованный ключ в бинарный файл."""
    try:
        with open(output_path, "wb") as f:
            f.write(encrypted_key)
    except IOError as e:
        print(f"Ошибка сохранения ключа в файл '{output_path}': {e}")
        sys.exit(1)


def read_encrypted_text(path_file: str) -> bytes:
    """Читает бинарные данные из файла."""
    try:
        with open(path_file, "rb") as t:
            encrypted_text = t.read()
            return encrypted_text
    except FileNotFoundError:
        print(f"Ошибка: Файл зашифрованных данных '{path_file}' не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка чтения файла '{path_file}': {e}")
        sys.exit(1)
