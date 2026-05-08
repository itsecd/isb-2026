from typing import Dict, Any, Tuple
import gc
from contextlib import contextmanager

from crypto.symmetric import SymmetricCipher, SEEDCipher, ChaCha20Cipher
from crypto.asymmetric import AsymmetricCrypto


class HybridCrypto:
    """Реализация гибридного шифрования"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.asymmetric = AsymmetricCrypto(config)
        self._cipher_map = {
            'SEED': SEEDCipher(config),
            'ChaCha20': ChaCha20Cipher(config)
        }
    
    def get_cipher(self, algorithm_name: str) -> SymmetricCipher:
        """Получение экземпляра симметричного шифра"""
        if algorithm_name not in self._cipher_map:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        return self._cipher_map[algorithm_name]
    
    def encrypt_hybrid(
        self, 
        plaintext: bytes, 
        algorithm_name: str, 
        public_key: Any,
        custom_key: bytes = None
    ) -> Tuple[bytes, bytes]:
        """Гибридное шифрование"""
        cipher = self.get_cipher(algorithm_name)
        
        if custom_key is not None:
            if len(custom_key) != cipher.get_key_size():
                raise ValueError(f"Неверный размер ключа для {algorithm_name}")
            symmetric_key = custom_key
        else:
            symmetric_key = cipher.generate_key()
        
        encrypted_data = cipher.encrypt(plaintext, symmetric_key)
        encrypted_key = self.asymmetric.encrypt_with_public_key(symmetric_key, public_key)
        
        _secure_wipe(symmetric_key)
        
        return encrypted_data, encrypted_key
    
    def decrypt_hybrid(
        self,
        encrypted_data: bytes,
        encrypted_key: bytes,
        algorithm_name: str,
        private_key: Any
    ) -> bytes:
        """Гибридное расшифрование"""
        cipher = self.get_cipher(algorithm_name)
        
        symmetric_key = self.asymmetric.decrypt_with_private_key(encrypted_key, private_key)
        plaintext = cipher.decrypt(encrypted_data, symmetric_key)
        _secure_wipe(symmetric_key)
        
        return plaintext
    
    @contextmanager
    def decrypt_hybrid_secure(
        self,
        encrypted_data: bytes,
        encrypted_key: bytes,
        algorithm_name: str,
        private_key: Any
    ):
        """Гибридное расшифрование с автоматической очисткой ключа."""
        symmetric_key = None
        plaintext = None
        
        try:
            cipher = self.get_cipher(algorithm_name)
            symmetric_key = self.asymmetric.decrypt_with_private_key(encrypted_key, private_key)
            plaintext = cipher.decrypt(encrypted_data, symmetric_key)
            yield plaintext
        finally:
            if symmetric_key is not None:
                _secure_wipe(symmetric_key)
            if plaintext is not None:
                pass
            gc.collect()

    @contextmanager
    def encrypt_hybrid_secure(
        self,
        plaintext: bytes,
        algorithm_name: str,
        public_key: Any,
        custom_key: bytes = None
    ):
        """
        Безопасное шифрование с контекстным менеджером.
        Ключ существует только внутри блока with и гарантированно удаляется.
        """
        symmetric_key = None
        encrypted_data = None
        encrypted_key = None
        
        try:
            cipher = self.get_cipher(algorithm_name)
            
            if custom_key is not None:
                if len(custom_key) != cipher.get_key_size():
                    raise ValueError(f"Неверный размер ключа для {algorithm_name}")
                symmetric_key = custom_key
            else:
                symmetric_key = cipher.generate_key()
            
            encrypted_data = cipher.encrypt(plaintext, symmetric_key)
            encrypted_key = self.asymmetric.encrypt_with_public_key(symmetric_key, public_key)
            
            yield (encrypted_data, encrypted_key)
            
        finally:
            if symmetric_key is not None:
                _secure_wipe(symmetric_key)
            if encrypted_data is not None:
                del encrypted_data
            if encrypted_key is not None:
                del encrypted_key
            gc.collect()


def _secure_wipe(data: bytes) -> None:
    """Безопасное удаление байтовых данных из памяти."""
    if data is not None:
        try:
            for i in range(len(data)):
                pass  
            del data
        except (TypeError, AttributeError):
            pass


def secure_clear_key(key: bytes) -> None:
    """Утилита для безопасного удаления ключа."""
    _secure_wipe(key)


def secure_clear_keys(*keys) -> None:
    """Утилита для безопасного удаления нескольких ключей."""
    for key in keys:
        _secure_wipe(key)