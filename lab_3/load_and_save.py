from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

def write_symmetric_key(symmetric_key: bytes, symmetric_path:str) -> None:
    """
    Сериализация симметричного ключа в файл
    Входные данные:
    symmetric_key - зашифрованный симметричный ключ шифрования
    symmetric_path - путь к сохранению ключа
    Сохраняет ключ в файл
    Возвращает:
    None
    """
    try:
        with open(symmetric_path, 'wb') as key_file:
            key_file.write(symmetric_key)
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def write_asymmetric_key(public_key:RSAPublicKey, private_key:RSAPrivateKey, public_path:str, private_path:str) -> None:
    """
    Сериализация асимметричных ключей в файл
    Входные данные:
    public_key - открытый RSA ключ
    private_key - закрытый RSA ключ
    public_path - зашифрованный симметричный ключ шифрования
    private_path - путь к сохранению ключа
    Сохраняет ключи в файл
    Возвращает:
    None
    """
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
    """
    Чтение ключа из файла
    Входные данные:
    symmetric_path - путь к симметричному ключу
    Возвращает:
    Зашифрованный симметричный ключ шифрования (bytes)
    """
    try:
        with open(symmetric_key_path, mode='rb') as key_file: 
            key = key_file.read()
            return key
    except Exception as ex:
        print(f"Ошибка!: {ex}")

def read_asymmetric_key(public_key_path:str, private_key_path) -> tuple:
    """
    Чтение RSA ключей из файлов
    Входные данные:
    public_key_path - путь к открытому RSA ключу
    private_key_path - путь к закрытому RSA ключу
    Возвращает:
    Зашифрованный симметричный ключ шифрования (bytes)
    """
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
    """
    Чтение текста из файла
    Входные данные:
    initial_file_path - путь к файлу с текстом
    Возвращает:
    Текст (bytes)
    """
    try:
        with open(initial_file_path, 'rb') as f:
            return f.read()
    except Exception as ex:
        print(f"Ошибка!: {ex}")
        return b""
    
def write_text(text: bytes,  enc_file_path: str) -> None:
    """
    Запись расшифрованного текста в файл
    Входные данные:
    text - текстом
    enc_file_path - путь к сохранению файла
    Сохраняет текст
    Возвращает:
    None
    """
    try:
        with open(enc_file_path, 'wb') as f:
            f.write(text)
    except Exception as ex:
        print(f"Ошибка!: {ex}")