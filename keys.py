"""
Модуль генерации ключей для гибридной криптосистемы RSA + 3DES.
"""

import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from utils import save_bin_data


def _generate_symmetric_key(key_len_bytes: int, algo_name: str) -> bytes:
    """
    Генерирует симметричный ключ заданной длины.

    Args:
        key_len_bytes: Длина ключа в байтах.
        algo_name: Название алгоритма для вывода в лог.

    Returns:
        Сгенерированные байты ключа.
    """
    sym_key = os.urandom(key_len_bytes)
    print(f"[INFO] Симметричный ключ ({algo_name}) сгенерирован. "
          f"Длина: {len(sym_key) * 8} бит.")
    return sym_key


def _generate_rsa_keys() -> rsa.RSAPrivateKey:
    """
    Генерирует пару ключей RSA (2048 бит).

    Returns:
        Объект закрытого ключа RSA.

    Raises:
        Exception: При ошибке генерации.
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        print("[INFO] Ключи RSA (2048 бит, e=65537) сгенерированы.")
        return private_key
    except Exception as e:
        print(f"[ERROR] Ошибка генерации RSA: {e}")
        raise


def _serialize_and_save_private_key(private_key: rsa.RSAPrivateKey, path: str) -> None:
    """
    Сериализует закрытый ключ в PEM и сохраняет в файл.

    Args:
        private_key: Закрытый ключ RSA.
        path: Путь для сохранения файла.

    Raises:
        Exception: При ошибке сериализации или записи.
    """
    try:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        save_bin_data(private_pem, path)
    except Exception as e:
        print(f"[ERROR] Ошибка сериализации закрытого ключа: {e}")
        raise


def _serialize_and_save_public_key(private_key: rsa.RSAPrivateKey, path: str) -> None:
    """
    Извлекает открытый ключ, сериализует в PEM и сохраняет.

    Args:
        private_key: Закрытый ключ RSA (из него берется открытый).
        path: Путь для сохранения файла.

    Raises:
        Exception: При ошибке сериализации или записи.
    """
    try:
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        save_bin_data(public_pem, path)
    except Exception as e:
        print(f"[ERROR] Ошибка сериализации открытого ключа: {e}")
        raise


def _encrypt_and_save_symmetric_key(public_key: rsa.RSAPublicKey, 
                                    sym_key: bytes, 
                                    path: str) -> None:
    """
    Шифрует симметричный ключ открытым ключом RSA (OAEP-SHA256) и сохраняет.

    Args:
        public_key: Открытый ключ RSA.
        sym_key: Байты симметричного ключа.
        path: Путь для сохранения зашифрованного ключа.

    Raises:
        Exception: При ошибке шифрования или записи.
    """
    try:
        encrypted_sym_key = public_key.encrypt(
            sym_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        save_bin_data(encrypted_sym_key, path)
    except Exception as e:
        print(f"[ERROR] Ошибка шифрования симметричного ключа: {e}")
        raise


def generate_keys(len_bits: int, pub_key_path: str, priv_key_path: str, enc_key_path: str) -> None:
    """
    Полный цикл генерации ключей гибридной системы.

    Координирует создание симметричного ключа, пары RSA и шифрование
    симметричного ключа. Использует match/case для выбора параметров.

    Args:
        len_bits: Длина симметричного ключа (64, 128 или 192).
        pub_key_path: Путь для открытого ключа RSA.
        priv_key_path: Путь для закрытого ключа RSA.
        enc_key_path: Путь для зашифрованного симметричного ключа.

    Raises:
        ValueError: Если длина ключа недопустима.
    """
    print("[STEP 1] Начало генерации ключей...")

    # Выбор параметров через match/case
    match len_bits:
        case 64:
            print("[WARN] Алгоритм DES удален из cryptography >= 42.0. "
                  "Используется 3DES с ключом 128 бит (16 байт).")
            key_len_bytes = 16
            algo_name = "3DES (2-key, эмуляция 64-bit)"
        case 128:
            key_len_bytes = 16
            algo_name = "3DES (2-key)"
        case 192:
            key_len_bytes = 24
            algo_name = "3DES (3-key)"
        case _:
            raise ValueError(
                f"Неподдерживаемая длина ключа: {len_bits}. "
                "Допустимые значения: 64, 128, 192."
            )

    # Последовательный вызов подфункций
    sym_key = _generate_symmetric_key(key_len_bytes, algo_name)
    
    private_key = _generate_rsa_keys()
    
    _serialize_and_save_private_key(private_key, priv_key_path)
    
    _serialize_and_save_public_key(private_key, pub_key_path)
    
    # Для шифрования нужен именно открытый ключ
    public_key = private_key.public_key()
    _encrypt_and_save_symmetric_key(public_key, sym_key, enc_key_path)

    print("[STEP 1] Генерация ключей завершена успешно.\n")
