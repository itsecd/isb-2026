import json
from cryptography.hazmat.primitives import serialization 
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey



def load_private_key(path_to_private: str) -> RSAPrivateKey:
    """
    Загрузка закрытого ключа
    """
    with open(path_to_private, 'rb') as pem_in:
        private_bytes = pem_in.read()
    
    private_key = load_pem_private_key(
        private_bytes,
        password=None 
    )
    
    return private_key

def load_public_key(path_to_public: str):
    """
    Загрузка открытого ключа RSA из файла
    """
    with open(path_to_public, 'rb') as pem_in:
        public_bytes = pem_in.read()
    
    
    public_key = load_pem_public_key(public_bytes)
    return public_key

def load_encrypt_symmetric_key(path_to_sym_key:str)-> bytes:
    """
    Загрузка симметричного ключа 
    """
    with open(path_to_sym_key, mode='rb') as key_file: 
        content = key_file.read()
    return content


def load_json(path_to_json: str):
    """
    Загрузка настроек из json
    """
    with open(path_to_json) as json_file:
        return json.load(json_file)
    

def read_text_file(filepath: str) -> str:
    """Чтение исходного текста из файла"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_text_file(text: str, filepath: str) -> None:
    """Запись расшифрованного текста в файл"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def read_binary_file(filepath: str) -> bytes:
    """Чтение бинарных (зашифрованных) данных из файла"""
    with open(filepath, 'rb') as f:
        return f.read()

def write_binary_file(data: bytes, filepath: str) -> None:
    """Запись бинарных (зашифрованных) данных в файл"""
    with open(filepath, 'wb') as f:
        f.write(data)
    


def save_asym_keys(private_key, public_key, path_private: str, path_public: str) -> None:
    """
    Сохранение ключей для асимметричного алгоритма 
    """
   
    with open(path_private, 'wb') as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()  
            )
        )

   
    with open(path_public, 'wb') as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    

def save_symmetric_key(encrypted_key: bytes,  output_path: str) -> None:
    """
    Сохранение ключа для симметричного алгоритма 
    """
    with open(output_path, 'wb') as f:
        f.write(encrypted_key)