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


def load_private_key(private_way: str) -> rsa.RSAPrivateKey:
    """Загружает закрытый ключ из файла."""
    with open(private_way, "rb") as pem_in:
        private_bytes = pem_in.read()
        private_key = load_pem_private_key(private_bytes, password=None)
        return private_key


def read_file(path_file: str) -> str:
    """Читает текст из файла."""
    with open(path_file, "r", encoding="utf-8") as t:
        text = t.read()
        return text


def write_text_file(text: str, file_path: str) -> None:
    """Записывает текст в файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


def save_symmetric_key(encrypted_key: bytes, output_path: str) -> None:
    """Сохраняет зашифрованный ключ в бинарный файл."""
    with open(output_path, "wb") as f:
        f.write(encrypted_key)


def read_encrypted_text(path_file: str) -> bytes:
    """Читает бинарные данные из файла."""
    with open(path_file, "rb") as t:
        encrypted_text = t.read()
        return encrypted_text
