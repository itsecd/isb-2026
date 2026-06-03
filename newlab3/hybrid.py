from symmetric import SymmetricCipher
from asymmetric import AsymmetricCipher
from file_utils import FileService


class HybridCryptoSystem:
    """Оркестратор для реализации комплексных сценариев работы гибридной криптосистемы.
    
    Объединяет симметричное (AES) и асимметричное (RSA) шифрование для обеспечения
    эффективного и безопасного шифрования больших объемов данных.
    
    Сценарии использования:
    1. Генерация ключей: создание AES-ключа и пары RSA-ключей
    2. Шифрование файла: использование RSA для шифрования AES-ключа
    3. Расшифрование файла: использование RSA для расшифрования AES-ключа
    """
    
    def __init__(self):
        """Инициализирует гибридную криптосистему с сервисом для работы с файлами."""
        self._file_service = FileService()
    
    def run_key_generation(
        self,
        encrypted_key_path: str,
        public_key_path: str,
        private_key_path: str,
        aes_key_size: int,
        rsa_key_size: int,
        rsa_public_exponent: int,
    ) -> None:
        """Выполняет полный цикл генерации всех необходимых ключей.
        
        Процесс включает:
        1. Генерацию симметричного AES-ключа
        2. Генерацию асимметричной пары RSA-ключей
        3. Сохранение RSA-ключей на диск
        4. Шифрование AES-ключа с помощью открытого RSA-ключа
        5. Сохранение зашифрованного AES-ключа
        
        Args:
            encrypted_key_path (str): Путь для сохранения зашифрованного AES-ключа.
            public_key_path (str): Путь для сохранения открытого RSA-ключа.
            private_key_path (str): Путь для сохранения закрытого RSA-ключа.
            aes_key_size (int): Размер AES-ключа в битах (128, 192 или 256).
            rsa_key_size (int): Размер RSA-ключа в битах (минимум 2048).
            rsa_public_exponent (int): Открытая экспонента RSA (3 или 65537).
            
        Example:
            >>> crypto = HybridCryptoSystem()
            >>> crypto.run_key_generation(
            ...     "keys/encrypted_aes.bin",
            ...     "keys/public.pem",
            ...     "keys/private.pem",
            ...     aes_key_size=256,
            ...     rsa_key_size=4096,
            ...     rsa_public_exponent=65537
            ... )
        """
        sym = SymmetricCipher(aes_key_size)
        asym = AsymmetricCipher(rsa_key_size, rsa_public_exponent)
        
        aes_key = sym.generate_key()
        priv_key, pub_key = asym.generate_pair()
        
        self._file_service.write_bytes(public_key_path, asym.serialize_public_key(pub_key))
        self._file_service.write_bytes(private_key_path, asym.serialize_private_key(priv_key))
        
        enc_aes_key = asym.encrypt_session_key(aes_key, pub_key)
        self._file_service.write_bytes(encrypted_key_path, enc_aes_key)
    
    def run_encryption(
        self, input_path: str, private_key_path: str, encrypted_key_path: str, output_path: str
    ) -> None:
        """Шифрует файл, используя сохраненные ключи.
        
        Процесс шифрования:
        1. Загрузка закрытого RSA-ключа для расшифрования AES-ключа
        2. Расшифрование AES-ключа с помощью RSA
        3. Чтение исходного файла
        4. Шифрование данных с помощью AES
        5. Сохранение зашифрованного файла
        
        Args:
            input_path (str): Путь к исходному файлу для шифрования.
            private_key_path (str): Путь к закрытому RSA-ключу.
            encrypted_key_path (str): Путь к зашифрованному AES-ключу.
            output_path (str): Путь для сохранения зашифрованного файла.
            
        Example:
            >>> crypto = HybridCryptoSystem()
            >>> crypto.run_encryption(
            ...     "documents/secret.txt",
            ...     "keys/private.pem",
            ...     "keys/encrypted_aes.bin",
            ...     "documents/secret.encrypted"
            ... )
        """
        asym = AsymmetricCipher()
        sym = SymmetricCipher()
        
        priv_bytes = self._file_service.read_bytes(private_key_path)
        priv_key = asym.load_private_key(priv_bytes)
        
        enc_key_bytes = self._file_service.read_bytes(encrypted_key_path)
        aes_key = asym.decrypt_session_key(enc_key_bytes, priv_key)
        
        source_data = self._file_service.read_bytes(input_path)
        encrypted_data = sym.encrypt(source_data, aes_key)
        self._file_service.write_bytes(output_path, encrypted_data)
    
    def run_decryption(
        self, input_path: str, private_key_path: str, encrypted_key_path: str, output_path: str
    ) -> None:
        """Расшифровывает файл, используя сохраненные ключи.
        
        Процесс расшифрования:
        1. Загрузка закрытого RSA-ключа для расшифрования AES-ключа
        2. Расшифрование AES-ключа с помощью RSA
        3. Чтение зашифрованного файла
        4. Расшифрование данных с помощью AES
        5. Сохранение расшифрованного файла
        
        Args:
            input_path (str): Путь к зашифрованному файлу.
            private_key_path (str): Путь к закрытому RSA-ключу.
            encrypted_key_path (str): Путь к зашифрованному AES-ключу.
            output_path (str): Путь для сохранения расшифрованного файла.
            
        Example:
            >>> crypto = HybridCryptoSystem()
            >>> crypto.run_decryption(
            ...     "documents/secret.encrypted",
            ...     "keys/private.pem",
            ...     "keys/encrypted_aes.bin",
            ...     "documents/secret_decrypted.txt"
            ... )
        """
        asym = AsymmetricCipher()
        sym = SymmetricCipher()
        
        priv_bytes = self._file_service.read_bytes(private_key_path)
        priv_key = asym.load_private_key(priv_bytes)
        
        enc_key_bytes = self._file_service.read_bytes(encrypted_key_path)
        aes_key = asym.decrypt_session_key(enc_key_bytes, priv_key)
        
        encrypted_data = self._file_service.read_bytes(input_path)
        decrypted_data = sym.decrypt(encrypted_data, aes_key)
        self._file_service.write_bytes(output_path, decrypted_data)
