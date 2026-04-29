from cryptography.hazmat.primitives.serialization import load_pem_private_key
import json

def load_private(path_to_private: str) -> RSAPrivateKey:
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

def load_encrypt_symmetric_key(path_to_sym_key:str)-> bytes:
    """
    Загрузка симметричного ключа 
    """
    with open(path_to_sym_key, mode='rb') as key_file: 
        content = key_file.read()
    return content


def load_json(path_to_json):
    


def main():
    """
    основная функция программы
    """


