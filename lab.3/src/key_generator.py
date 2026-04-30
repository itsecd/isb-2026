import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from .utils import generate_symmetric_key, save_symmetric_key, load_symmetric_key


def generate_asymmetric_keys(key_size: int = 2048) -> tuple:
    """Генерация пары RSA ключей"""
    print(" Генерация асимметричных ключей")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    print(f" Ключи сгенерированы (размер: {key_size} бит)")
    return private_key, public_key


def save_public_key(public_key, filepath: str) -> None:
    """Сохранение открытого RSA ключа в PEM файл"""
    with open(filepath, 'wb') as public_out:
        public_out.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    print(f" Открытый ключ сохранен: {filepath}")


def save_private_key(private_key, filepath: str) -> None:
    """Сохранение приватного RSA ключа в PEM файл """
    with open(filepath, 'wb') as private_out:
        private_out.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print(f" Приватный ключ сохранен: {filepath}")


def load_public_key(filepath: str):
    """Загрузка открытого RSA ключа из PEM файла"""
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    with open(filepath, 'rb') as pem_in:
        public_bytes = pem_in.read()
    return load_pem_public_key(public_bytes)


def load_private_key(filepath: str):
    """Загрузка приватного RSA ключа из PEM файла"""
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    with open(filepath, 'rb') as pem_in:
        private_bytes = pem_in.read()
    return load_pem_private_key(private_bytes, password=None)


def encrypt_symmetric_key_with_rsa(symmetric_key: bytes, public_key_path: str, output_path: str) -> None:
    """Шифрование симметричного ключа открытым RSA ключом и сохранение"""
    print(" Загрузка открытого RSA ключа...")
    public_key = load_public_key(public_key_path)
    
    print(" Шифрование симметричного ключа RSA")
    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    with open(output_path, 'wb') as f:
        f.write(encrypted_key)
    print(f" Зашифрованный симметричный ключ сохранен: {output_path}")


def run_key_generation(public_key_path: str, private_key_path: str, 
                       symmetric_key_path: str, encrypted_symmetric_key_path: str) -> None:
    """
    Запуск режима генерации ключей
    
    Входные параметры:
        1) путь, по которому сохранить открытый ключ (асимметричный)
        2) путь, по которому сохранить приватный ключ (асимметричный)
        3) путь, по которому сохранить симметричный ключ
    
    """
    print("\n" + "="*60)
    print("Режим 1: Генерация ключей системы")
    print("="*60)
    
    print("\n Генерация ключа для симметричного алгоритма (Camellia)")
    symmetric_key = generate_symmetric_key(32) 
    save_symmetric_key(symmetric_key, symmetric_key_path)
    
    print("\n Генерация ключей для асимметричного алгоритма (RSA)")
    private_key, public_key = generate_asymmetric_keys(2048)
    
    print("\n Сохранение ключей...")
    save_public_key(public_key, public_key_path)
    save_private_key(private_key, private_key_path)
    
    print("\n Зашифрование симметричного ключа открытым ключом...")
    encrypt_symmetric_key_with_rsa(symmetric_key, public_key_path, encrypted_symmetric_key_path)
    
    print("\n" + "="*60)
    print(" Генерация ключей завершена!")
    print(f" Открытый ключ RSA: {public_key_path}")
    print(f" Приватный ключ RSA: {private_key_path}")
    print(f" Симметричный ключ (Camellia): {symmetric_key_path}")
    print(f" Зашифрованный симметричный ключ: {encrypted_symmetric_key_path}")
    print("="*60)