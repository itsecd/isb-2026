from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

def write_symmetric_key(symmetric_key: bytes, symmetric_path:str) -> None:
    """сериализация ссиметричного ключа в файл"""
    try:
        with open(symmetric_path, 'wb') as key_file:
            key_file.write(symmetric_key)
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def write_asymmetric_key(public_key:RSAPublicKey, private_key:RSAPrivateKey, public_path:str, private_path:str) -> None:
    """сериализация ассиметричных ключей в файл"""
    try:
        with open(public_path, 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo))
        with open(private_path, 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()))
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def read_symmetric_key(symmetric_key_path:str) -> bytes:
    """чтение ключа из файла"""
    try:
        with open(symmetric_key_path, mode='rb') as key_file: 
            key = key_file.read()
            return key
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def read_asymmetric_key(public_key_path:str, private_key_path) -> tuple:
    """чтение RSA ключей из файлов"""
    try:
        with open(public_key_path, 'rb') as pem_in:
            public_bytes = pem_in.read()
            public_key = load_pem_public_key(public_bytes)
        with open(private_key_path, 'rb') as pem_in:
            private_bytes = pem_in.read()
            private_key = load_pem_private_key(private_bytes,password=None,)
        return public_key, private_key
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def read_text(initial_file_path:str) -> bytes:
    """чтение текста из файла"""
    try:
        with open(initial_file_path, 'rb') as f:
            return f.read()
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return b""
    
def write_text(text: bytes,  enc_file_path: str) -> None:
    """запись расшифрованного текста в файл"""
    try:
        with open(enc_file_path, 'wb') as f:
            f.write(text)
    except Exception as ex:
        print(f"Ошибка!: {ex}")