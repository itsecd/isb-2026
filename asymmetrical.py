import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

from auxiliary_functions import write_file, read_file

def generate_rsa_keys(settings):
    """Генерирует пару RSA ключей."""
    private_key = rsa.generate_private_key(
        public_exponent=settings['public_exponent'],
        key_size=settings['key_size'],
        backend=default_backend()
    )
    public_key = private_key.public_key()
    print("Пара асимметричных ключей RSA сгенерирована.")
    
    return private_key, public_key

def save_rsa_keys(settings, private_key, public_key):
    """Сохраняет RSA ключи в файлы."""
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

def encrypt_symmetric_key(settings, symmetric_key):
    """Шифрует симметричный ключ с помощью RSA открытого ключа."""
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
    """Расшифровывает симметричный ключ с помощью RSA закрытого ключа."""
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