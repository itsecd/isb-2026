import os
from typing import Dict, Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import padding  
from cryptography.hazmat.backends import default_backend


class SymmetricCipher:
    """Базовый класс для симметричных шифров"""
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        raise NotImplementedError("Метод encrypt должен быть реализован")
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        raise NotImplementedError("Метод decrypt должен быть реализован")
    
    def generate_key(self) -> bytes:
        raise NotImplementedError("Метод generate_key должен быть реализован")
    
    def get_key_size(self) -> int:
        raise NotImplementedError("Метод get_key_size должен быть реализован")


class SEEDCipher(SymmetricCipher):
    """Реализация SEED шифрования через CBC режим с PKCS7 padding"""
    
    def __init__(self, config: Dict[str, Any]):
        try:
            crypto_section = config.get('crypto')
            if crypto_section is None:
                raise KeyError("Секция 'crypto' не найдена в конфигурации")
            
            seed_section = crypto_section.get('seed')
            if seed_section is None:
                raise KeyError("Секция 'seed' не найдена в конфигурации")
            
            if not isinstance(seed_section, (list, tuple)) or len(seed_section) < 2:
                raise ValueError("Секция 'seed' должна содержать минимум 2 элемента: [key_size, block_size]")
            
            self._key_size = seed_section[0]     
            self._block_size = seed_section[1]    
            
            if not isinstance(self._key_size, int) or self._key_size <= 0:
                raise ValueError(f"Размер ключа SEED должен быть положительным целым числом")
            
            if not isinstance(self._block_size, int) or self._block_size <= 0:
                raise ValueError(f"Размер блока SEED должен быть положительным целым числом")
            
            if self._key_size != 16:
                raise ValueError(f"SEED требует ключ 128 бит (16 байт)")
            
            if self._block_size != 16:
                raise ValueError(f"SEED требует блок 128 бит (16 байт)")
            
            self.backend = default_backend()
            
        except KeyError as e:
            raise ValueError(f"Ошибка конфигурации SEED: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка инициализации SEED: {e}")
    
    def generate_key(self) -> bytes:
        try:
            return os.urandom(self._key_size)
        except Exception as e:
            raise RuntimeError(f"Не удалось сгенерировать ключ SEED: {e}")
    
    def get_key_size(self) -> int:
        return self._key_size
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        try:
            if not isinstance(plaintext, bytes):
                raise TypeError(f"plaintext должен быть bytes")
            
            if not isinstance(key, bytes):
                raise TypeError(f"key должен быть bytes")
            
            if len(key) != self._key_size:
                raise ValueError(f"Ключ должен быть {self._key_size} байт")
            
            if len(plaintext) == 0:
                raise ValueError("Нет данных для шифрования")
            
            iv = os.urandom(self._block_size)
            
            padder = padding.PKCS7(self._block_size * 8).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv), backend=self.backend)
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            return iv + encrypted
            
        except (TypeError, ValueError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Ошибка при шифровании SEED: {e}")
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        try:
            if not isinstance(ciphertext, bytes):
                raise TypeError(f"ciphertext должен быть bytes")
            
            if not isinstance(key, bytes):
                raise TypeError(f"key должен быть bytes")
            
            if len(key) != self._key_size:
                raise ValueError(f"Ключ должен быть {self._key_size} байт")
            
            if len(ciphertext) < self._block_size:
                raise ValueError(f"Шифротекст слишком короткий")
            
            iv = ciphertext[:self._block_size]
            encrypted = ciphertext[self._block_size:]
            
            if len(encrypted) == 0:
                raise ValueError("Нет зашифрованных данных")
            
            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
            
            if len(decrypted_padded) == 0:
                raise RuntimeError("Результат расшифрования пуст")
            
            unpadder = padding.PKCS7(self._block_size * 8).unpadder()
            plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()
            
            return plaintext
            
        except (TypeError, ValueError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Ошибка при расшифровании SEED: {e}")


class ChaCha20Cipher(SymmetricCipher):
    """Реализация ChaCha20 шифрования"""
    
    def __init__(self, config: Dict[str, Any]):
        try:
            crypto_section = config.get('crypto')
            if crypto_section is None:
                raise KeyError("Секция 'crypto' не найдена в конфигурации")
            
            chacha_section = crypto_section.get('chacha20')
            if chacha_section is None:
                raise KeyError("Секция 'chacha20' не найдена в конфигурации")
            
            if not isinstance(chacha_section, (list, tuple)) or len(chacha_section) < 2:
                raise ValueError("Секция 'chacha20' должна содержать минимум 2 элемента: [key_size, nonce_size]")
            
            self._key_size = chacha_section[0]      
            self._nonce_size = chacha_section[1]    
            
            if not isinstance(self._key_size, int) or self._key_size <= 0:
                raise ValueError(f"Размер ключа ChaCha20 должен быть положительным целым числом, получено: {self._key_size}")
            
            if not isinstance(self._nonce_size, int) or self._nonce_size <= 0:
                raise ValueError(f"Размер nonce ChaCha20 должен быть положительным целым числом, получено: {self._nonce_size}")
            
            if self._key_size != 32:
                raise ValueError(f"ChaCha20 рекомендуется ключ 256 бит (32 байта), получено: {self._key_size}")
            
            if self._nonce_size != 12:
                raise ValueError(f"ChaCha20 рекомендуется nonce 96 бит (12 байт), получено: {self._nonce_size}")
            
        except KeyError as e:
            raise ValueError(f"Ошибка конфигурации ChaCha20: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка инициализации ChaCha20: {e}")
    
    def generate_key(self) -> bytes:
        try:
            return os.urandom(self._key_size)
        except Exception as e:
            raise RuntimeError(f"Не удалось сгенерировать ключ ChaCha20: {e}")
    
    def get_key_size(self) -> int:
        return self._key_size
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        try:
            if not isinstance(plaintext, bytes):
                raise TypeError(f"plaintext должен быть bytes, получен {type(plaintext)}")
            
            if not isinstance(key, bytes):
                raise TypeError(f"key должен быть bytes, получен {type(key)}")
            
            if len(key) != self._key_size:
                raise ValueError(f"Ключ должен быть {self._key_size} байт, получено {len(key)} байт")
            
            if len(plaintext) == 0:
                raise ValueError("Нет данных для шифрования")
            
            nonce = os.urandom(self._nonce_size)
            
            try:
                chacha = ChaCha20Poly1305(key)
            except Exception as e:
                raise RuntimeError(f"Не удалось создать шифр ChaCha20: {e}")
            
            try:
                ciphertext = chacha.encrypt(nonce, plaintext, None)
            except Exception as e:
                raise RuntimeError(f"Ошибка при шифровании ChaCha20: {e}")
            
            return nonce + ciphertext
            
        except (TypeError, ValueError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Неожиданная ошибка при шифровании ChaCha20: {e}")
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        try:
            if not isinstance(ciphertext, bytes):
                raise TypeError(f"ciphertext должен быть bytes, получен {type(ciphertext)}")
            
            if not isinstance(key, bytes):
                raise TypeError(f"key должен быть bytes, получен {type(key)}")
            
            if len(key) != self._key_size:
                raise ValueError(f"Ключ должен быть {self._key_size} байт, получено {len(key)} байт")
            
            if len(ciphertext) < self._nonce_size:
                raise ValueError(f"Шифротекст слишком короткий: минимум {self._nonce_size} байт, получено {len(ciphertext)} байт")
            
            nonce = ciphertext[:self._nonce_size]
            encrypted = ciphertext[self._nonce_size:]
            
            if len(encrypted) == 0:
                raise ValueError("Нет зашифрованных данных")
            
            try:
                chacha = ChaCha20Poly1305(key)
            except Exception as e:
                raise RuntimeError(f"Не удалось создать дешифратор ChaCha20: {e}")
            
            try:
                plaintext = chacha.decrypt(nonce, encrypted, None)
            except Exception as e:
                raise ValueError(f"Ошибка расшифрования ChaCha20 (возможно неверный ключ или повреждены данные): {e}")
            
            if len(plaintext) == 0:
                raise RuntimeError("Результат расшифрования пуст")
            
            return plaintext
            
        except (TypeError, ValueError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Неожиданная ошибка при расшифровании ChaCha20: {e}")