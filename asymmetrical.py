import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

from auxiliary_functions import write_file, read_file

def generate_rsa_keys(settings):
    """
    Генерирует пару асимметричных ключей RSA.
    
    Входные данные:
        settings (dict): Словарь настроек, содержащий 'public_exponent' (int) и 'key_size' (int).
        
    Выходные данные:
        tuple: Кортеж (private_key, public_key) объектов ключей cryptography, или (None, None) в случае ошибки.
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=settings['public_exponent'],
            key_size=settings['key_size'],
            backend=default_backend()
        )
        public_key = private_key.public_key()
        print("Пара асимметричных ключей RSA сгенерирована.")
        return private_key, public_key
    except Exception as e:
        print(f"Ошибка генерации RSA ключей: {e}")
        return None, None

def save_rsa_keys(settings, private_key, public_key):
    """
    Сохраняет сгенерированные RSA ключи в файлы в формате PEM.
    
    Входные данные:
        settings (dict): Словарь настроек с путями 'private_key' и 'public_key'.
        private_key: Объект закрытого ключа RSA.
        public_key: Объект открытого ключа RSA.
        
    Выходные данные:
        bool: True если оба ключа успешно сохранены, False иначе.
    """
    try:
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        if not write_file(settings['private_key'], private_key_bytes):
            return False
        print(f"Закрытый ключ сохранен в: {settings['private_key']}")

        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        if not write_file(settings['public_key'], public_key_bytes):
            return False
        print(f"Открытый ключ сохранен в: {settings['public_key']}")
        
        return True
    except Exception as e:
        print(f"Ошибка сохранения RSA ключей: {e}")
        return False

def encrypt_symmetric_key(settings, symmetric_key):
    """
    Шифрует симметричный ключ с помощью открытого RSA ключа (OAEP padding).
    
    Входные данные:
        settings (dict): Словарь настроек с путями 'public_key' и 'symmetric_key_encrypted'.
        symmetric_key (bytes): Байтовая строка симметричного ключа.
        
    Выходные данные:
        bytes: Зашифрованный симметричный ключ, или None в случае ошибки.
    """
    public_key_pem = read_file(settings['public_key'])
    if public_key_pem is None:
        return None
    
    try:
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        if not write_file(settings['symmetric_key_encrypted'], encrypted_key):
            return None
        print(f"Зашифрованный симметричный ключ сохранен в: {settings['symmetric_key_encrypted']}")
        
        return encrypted_key
    except Exception as e:
        print(f"Ошибка шифрования симметричного ключа: {e}")
        return None

def decrypt_symmetric_key(settings):
    """
    Расшифровывает симметричный ключ с помощью закрытого RSA ключа.
    
    Входные данные:
        settings (dict): Словарь настроек с путями 'private_key' и 'symmetric_key_encrypted'.
        
    Выходные данные:
        bytes: Расшифрованный симметричный ключ, или None в случае ошибки.
    """
    private_key_pem = read_file(settings['private_key'])
    if private_key_pem is None:
        return None
    
    encrypted_key_data = read_file(settings['symmetric_key_encrypted'])
    if encrypted_key_data is None:
        return None

    try:
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        symmetric_key = private_key.decrypt(
            encrypted_key_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return symmetric_key
    except Exception as e:
        print(f"Ошибка расшифровки симметричного ключа: {e}")
        return None