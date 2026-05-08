from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import rsa
from crypto.asymmetric import AsymmetricCrypto
from utils.file_utils import FileManager


class KeyManager:
    
    def __init__(self, config: Dict[str, Any], file_manager: FileManager, private_path: str, public_path: str):
        self.config = config
        self.file_manager = file_manager
        self.asymmetric_crypto = AsymmetricCrypto(config)
        self._private_path = private_path
        self._public_path = public_path
    
    def ensure_rsa_keys_exist(self) -> None:
        """Проверяет существование ключей, генерирует если нет"""
        if not (self.file_manager.file_exists(self._private_path) and 
                self.file_manager.file_exists(self._public_path)):
            self._generate_and_save_rsa_keys()
    
    def _generate_and_save_rsa_keys(self) -> None:
        """Генерирует и сохраняет RSA ключи (без пароля)"""
        private_key, public_key = self.asymmetric_crypto.generate_rsa_keypair()
        
        private_bytes = self.asymmetric_crypto.save_private_key_to_bytes(private_key)
        public_bytes = self.asymmetric_crypto.save_public_key_to_bytes(public_key)
        
        self.file_manager.write_file(self._private_path, private_bytes, binary=True)
        self.file_manager.write_file(self._public_path, public_bytes, binary=True)
        
        del private_key
        del public_key
    
    def load_public_key(self) -> rsa.RSAPublicKey:
        """Загружает публичный ключ из файла"""
        public_bytes = self.file_manager.read_file(self._public_path, binary=True)
        public_key = self.asymmetric_crypto.load_public_key(public_bytes)
        del public_bytes
        return public_key
    
    def load_private_key(self) -> rsa.RSAPrivateKey:
        """Загружает приватный ключ из файла (без пароля)"""
        private_bytes = self.file_manager.read_file(self._private_path, binary=True)
        private_key = self.asymmetric_crypto.load_private_key(private_bytes)
        del private_bytes
        return private_key
    
    def create_symmetric_key(self, algorithm: str, key_bytes: Optional[bytes] = None) -> bytes:
        """Создает симметричный ключ для указанного алгоритма"""
        from crypto.hybrid import HybridCrypto
        hybrid = HybridCrypto(self.config)
        cipher = hybrid.get_cipher(algorithm)
        
        if key_bytes is not None:
            return key_bytes
        return cipher.generate_key()
    
    def secure_load_and_use_private_key(self, callback):
        """Безопасно загружает приватный ключ, передает его в callback,"""
        private_key = None
        try:
            private_key = self.load_private_key()
            return callback(private_key)
        finally:
            if private_key is not None:
                del private_key
            import gc
            gc.collect()