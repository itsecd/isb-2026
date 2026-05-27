import os
from typing import Tuple

from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from file_utils import FileService


class HybridCryptoError(Exception):
    """Базовое исключение для всей гибридной криптосистемы."""
    pass


class SymmetricCryptoError(HybridCryptoError):
    """Исключение для ошибок, возникающих при работе с симметричным шифрованием (AES)."""
    pass


class AsymmetricCryptoError(HybridCryptoError):
    """Исключение для ошибок, возникающих при работе с асимметричным шифрованием (RSA)."""
    pass


class SymmetricCipher:
    """Класс для управления симметричным шифрованием с использованием алгоритма AES-CBC."""

    def __init__(self, key_size: int = 256):
        """Инициализирует параметры симметричного шифра.

        Args:
            key_size (int): Размер ключа в битах (128, 192 или 256).
        """
        self._key_size = self._validate_key_size(key_size)

    def _validate_key_size(self, key_size: int) -> int:
        """Проверяет корректность размера ключа AES.

        Args:
            key_size (int): Размер ключа для проверки.

        Returns:
            int: Проверенный размер ключа.

        Raises:
            SymmetricCryptoError: Если размер ключа не поддерживается.
        """
        try:
            size = int(key_size)
        except (TypeError, ValueError) as exc:
            raise SymmetricCryptoError("Размер AES-ключа должен быть числом") from exc

        match size:
            case 128 | 192 | 256:
                return size
            case _:
                raise SymmetricCryptoError("Размер AES-ключа должен быть 128, 192 или 256 бит")

    def generate_key(self) -> bytes:
        """Генерирует случайный криптостойкий ключ AES.

        Returns:
            bytes: Сгенерированный сессионный ключ.
        """
        return os.urandom(self._key_size // 8)

    def encrypt(self, data: bytes, aes_key: bytes) -> bytes:
        """Шифрует данные алгоритмом AES в режиме CBC со случайным IV.

        Args:
            data (bytes): Открытый текст для шифрования.
            aes_key (bytes): Симметричный ключ AES.

        Returns:
            bytes: Вектор инициализации IV (16 байт) + шифртекст.

        Raises:
            SymmetricCryptoError: При ошибках шифрования или дополнения данных.
        """
        iv_size = algorithms.AES.block_size // 8
        iv = os.urandom(iv_size)
        
        try:
            padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(data) + padder.finalize()

            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            return iv + encrypted_data
        except ValueError as exc:
            raise SymmetricCryptoError("Ошибка добавления дополнения или AES-шифрования") from exc

    def decrypt(self, data: bytes, aes_key: bytes) -> bytes:
        """Расшифровывает данные AES-CBC, извлекая IV из начала последовательности.

        Args:
            data (bytes): Байты зашифрованного файла (IV + шифртекст).
            aes_key (bytes): Симметричный ключ AES.

        Returns:
            bytes: Расшифрованный текст без дополнения.

        Raises:
            SymmetricCryptoError: При неверном ключе, повреждении данных или паддинга.
        """
        iv_size = algorithms.AES.block_size // 8

        if len(data) < iv_size:
            raise SymmetricCryptoError("Зашифрованный файл слишком короткий для извлечения IV")

        iv = data[:iv_size]
        encrypted_data = data[iv_size:]

        try:
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
            return unpadder.update(decrypted_data) + unpadder.finalize()
        except ValueError as exc:
            raise SymmetricCryptoError("Ошибка расшифрования. Возможно, используется неверный ключ") from exc


class AsymmetricCipher:
    """Класс для управления асимметричным шифрованием и работы с ключами RSA."""

    def __init__(self, key_size: int = 2048, public_exponent: int = 65537):
        """Инициализирует параметры асимметричного шифра.

        Args:
            key_size (int): Длина ключа RSA в битах (не менее 2048).
            public_exponent (int): Открытая экспонента (3 или 65537).
        """
        self._key_size = self._validate_key_size(key_size)
        self._public_exponent = self._validate_exponent(public_exponent)

    def _validate_key_size(self, key_size: int) -> int:
        """Проверяет длину ключа RSA.

        Args:
            key_size (int): Длина ключа для проверки.

        Returns:
            int: Проверенная длина ключа.

        Raises:
            AsymmetricCryptoError: Если длина ключа неудовлетворительна.
        """
        try:
            size = int(key_size)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Размер RSA-ключа должен быть числом") from exc

        if size < 2048:
            raise AsymmetricCryptoError("Размер RSA-ключа должен быть не меньше 2048 бит")
        return size

    def _validate_exponent(self, exponent: int) -> int:
        """Проверяет значение открытой экспоненты с помощью паттерн-матчинга.

        Args:
            exponent (int): Значение экспоненты.

        Returns:
            int: Проверенное значение экспоненты.

        Raises:
            AsymmetricCryptoError: Если экспонента не поддерживается стандартами.
        """
        try:
            val = int(exponent)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Экспонента RSA должна быть числом") from exc

        match val:
            case 3 | 65537:
                return val
            case _:
                raise AsymmetricCryptoError("Открытая экспонента RSA должна быть 3 или 65537")

    def generate_pair(self) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """Генерирует пару открытого и закрытого ключей RSA.

        Returns:
            Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]: Кортеж объектов ключей.

        Raises:
            AsymmetricCryptoError: При сбое генерации.
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=self._public_exponent,
                key_size=self._key_size,
            )
            return private_key, private_key.public_key()
        except ValueError as exc:
            raise AsymmetricCryptoError("Не удалось сгенерировать пару ключей RSA") from exc

    def _get_oaep_padding(self) -> asym_padding.OAEP:
        """Возвращает стандартную конфигурацию дополнения OAEP.

        Returns:
            asym_padding.OAEP: Настройки дополнения с использованием SHA-256.
        """
        return asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

    def serialize_public_key(self, public_key: rsa.RSAPublicKey) -> bytes:
        """Преобразует открытый ключ в формат PEM.

        Args:
            public_key (rsa.RSAPublicKey): Объект открытого ключа.

        Returns:
            bytes: Сериализованные байты открытого ключа.
        """
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def serialize_private_key(self, private_key: rsa.RSAPrivateKey) -> bytes:
        """Преобразует закрытый ключ в формат PEM без пароля.

        Args:
            private_key (rsa.RSAPrivateKey): Объект закрытого ключа.

        Returns:
            bytes: Сериализованные байты закрытого ключа.
        """
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def load_private_key(self, key_data: bytes) -> rsa.RSAPrivateKey:
        """Загружает объект закрытого ключа из байтовой строки PEM.

        Args:
            key_data (bytes): Сериализованные байты ключа.

        Returns:
            rsa.RSAPrivateKey: Восстановленный объект закрытого ключа.

        Raises:
            AsymmetricCryptoError: При повреждении или неверном формате структуры ключа.
        """
        try:
            return serialization.load_pem_private_key(key_data, password=None)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Не удалось десериализовать закрытый RSA-ключ") from exc

    def load_public_key(self, key_data: bytes) -> rsa.RSAPublicKey:
        """Загружает объект открытого ключа из байтовой строки PEM.

        Args:
            key_data (bytes): Сериализованные байты ключа.

        Returns:
            rsa.RSAPublicKey: Восстановленный объект открытого ключа.

        Raises:
            AsymmetricCryptoError: При повреждении структуры открытого ключа.
        """
        try:
            return serialization.load_pem_public_key(key_data)
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Не удалось десериализовать открытый RSA-ключ") from exc

    def encrypt_session_key(self, aes_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        """Шифрует сессионный ключ AES с помощью открытого ключа RSA.

        Args:
            aes_key (bytes): Байты ключа AES.
            public_key (rsa.RSAPublicKey): Объект открытого ключа.

        Returns:
            bytes: Зашифрованный ключ AES.

        Raises:
            AsymmetricCryptoError: Если шифрование завершилось ошибкой.
        """
        try:
            return public_key.encrypt(aes_key, self._get_oaep_padding())
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Ошибка шифрования ключа алгоритмом RSA-OAEP") from exc

    def decrypt_session_key(self, encrypted_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        """Расшифровывает сессионный ключ AES с помощью закрытого ключа RSA.

        Args:
            encrypted_key (bytes): Зашифрованные байты сессионного ключа.
            private_key (rsa.RSAPrivateKey): Объект закрытого ключа.

        Returns:
            bytes: Расшифрованный ключ AES.

        Raises:
            AsymmetricCryptoError: Если расшифрование завершилось ошибкой.
        """
        try:
            return private_key.decrypt(encrypted_key, self._get_oaep_padding())
        except (TypeError, ValueError) as exc:
            raise AsymmetricCryptoError("Ошибка расшифрования ключа алгоритмом RSA-OAEP") from exc


class HybridCryptoSystem:
    """Высокоуровневый класс-оркестратор для реализации комплексных сценариев работы системы."""

    def __init__(self):
        """Инициализирует внутренний файловый сервис."""
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
        """Сценарий 1: Генерация асимметричной пары, сессионного ключа и сохранение зашифрованного секрета.

        Args:
            encrypted_key_path (str): Путь сохранения зашифрованного ключа AES.
            public_key_path (str): Путь сохранения открытого ключа RSA.
            private_key_path (str): Путь сохранения закрытого ключа RSA.
            aes_key_size (int): Размер ключа AES в битах.
            rsa_key_size (int): Размер ключа RSA в битах.
            rsa_public_exponent (int): Значение открытой экспоненты RSA.
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
        """Сценарий 2: Дешифрование симметричного сессионного ключа и зашифрование целевого файла.

        Args:
            input_path (str): Путь к исходному открытому тексту.
            private_key_path (str): Путь к закрытому ключу RSA.
            encrypted_key_path (str): Путь к зашифрованному файлу ключа AES.
            output_path (str): Путь сохранения зашифрованного бинарного файла.
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
        """Сценарий 3: Дешифрование сессионного ключа и полное восстановление исходного файла.

        Args:
            input_path (str): Путь к зашифрованному бинарному файлу.
            private_key_path (str): Путь к закрытому ключу RSA.
            encrypted_key_path (str): Путь к зашифрованному файлу ключа AES.
            output_path (str): Путь сохранения расшифрованного текстового файла.
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