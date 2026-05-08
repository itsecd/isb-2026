from typing import Optional, Dict, Any, Tuple
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


class AsymmetricCrypto:
    
    def __init__(self, config: Dict[str, Any]):
        rsa_section = config['crypto']['rsa']
        self._rsa_key_size = rsa_section[0]
        self._public_exponent = rsa_section[1]
        
        padding_section = rsa_section[2]
        self._padding_scheme = padding_section[0]
        self._label = padding_section[3]
        
        if self._label is not None and isinstance(self._label, str):
            self._label = self._label.encode('utf-8')
        
        self.backend = default_backend()
    
    def generate_rsa_keypair(self) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        private_key = rsa.generate_private_key(
            public_exponent=self._public_exponent,
            key_size=self._rsa_key_size,
            backend=self.backend
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def encrypt_with_public_key(self, data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        if not data:
            raise ValueError("Нет данных для шифрования")
        
        padding_scheme = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=self._label
        )
        
        return public_key.encrypt(data, padding_scheme)
    
    def decrypt_with_private_key(self, encrypted_data: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        if not encrypted_data:
            raise ValueError("Нет данных для расшифрования")
        
        padding_scheme = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=self._label
        )
        
        return private_key.decrypt(encrypted_data, padding_scheme)
    
    def load_private_key(self, key_data: bytes) -> rsa.RSAPrivateKey:
        """Загрузка приватного ключа из PEM (без пароля)"""
        return serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=self.backend
        )
    
    def load_public_key(self, key_data: bytes) -> rsa.RSAPublicKey:
        """Загрузка публичного ключа из PEM"""
        return serialization.load_pem_public_key(
            key_data,
            backend=self.backend
        )
    
    def save_private_key_to_bytes(self, private_key: rsa.RSAPrivateKey) -> bytes:
        """Сохранение приватного ключа в PEM"""
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    def save_public_key_to_bytes(self, public_key: rsa.RSAPublicKey) -> bytes:
        """Сохранение публичного ключа в PEM"""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )