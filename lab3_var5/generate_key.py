import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generating_symmetric_key() -> bytes: 
    """
    Геренирование ключа для симметричного алгоритма
    """
    key = os.urandom(32)
    return key


def generating_asymmetric_key() -> bytes:
    """
    Геренирование ключей для асимметричного алгоритма
    """
    keys = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def save_asym_keys(private_key, public_key, path_private: str, path_public: str) -> None:
    """
    Сохранение ключей для асимметричного алгоритма (например, RSA или Ed25519)
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
    

def encrypt_and_save_symmetric_key(symmetric_key: bytes, public_key, output_path: str) -> None:
    encrypted_key = public_key.encrypt(symmetric_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    
    with open(output_path, 'wb') as f:
        f.write(encrypted_key)

