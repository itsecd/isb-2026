import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

from auxiliary_functions import write_file

def generate_keys(settings):
    """Генерирует ключи и сохраняет их."""

    symmetric_key = os.urandom(settings['BLOCK_SIZE_BYTES'])
    print(f"Симметричный ключ SEED сгенерирован.")

    private_key = rsa.generate_private_key(
        public_exponent=settings['public_exponent'],
        key_size=settings['key_size'],
        backend=default_backend()
    )
    public_key = private_key.public_key()
    print("Пара асимметричных ключей сгенерирована.")

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    if not write_file(settings['private_key'], private_key_bytes):
        return
    print(f"Закрытый ключ сохранен в: {settings['private_key']}")

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if not write_file(settings['public_key'], public_key_bytes):
        return
    print(f"Открытый ключ сохранен в: {settings['public_key']}")

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    if not write_file(settings['symmetric_key_encrypted'], encrypted_symmetric_key):
        return
    print(f"Зашифрованный симметричный ключ сохранен в: {settings['symmetric_key_encrypted']}")

    print("Генерация ключей завершена")