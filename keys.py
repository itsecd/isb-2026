"""
Модуль генерации ключей гибридной криптосистемы RSA + 3DES.

Реализует создание симметричного ключа (с адаптацией под удаление DES
в cryptography >= 42.0), пары ключей RSA-2048 и шифрование симметричного
ключа алгоритмом RSA-OAEP-SHA256.
"""

import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from utils import save_bin_data


def generate_keys(
    len_bits: int,
    pub_key_path: str,
    priv_key_path: str,
    enc_key_path: str
) -> None:
    """
    Полный цикл генерации ключей гибридной системы.

    1. Генерирует симметричный ключ для 3DES.
       Для len_bits=64 используется 16 байт (т.к. DES удален из библиотеки).
    2. Генерирует пару RSA-2048 (e=65537).
    3. Сериализует ключи в PEM (TraditionalOpenSSL / SubjectPublicKeyInfo).
    4. Шифрует симметричный ключ через RSA-OAEP(SHA256) и сохраняет.

    Args:
        len_bits: Длина симметричного ключа (64, 128 или 192).
        pub_key_path: Путь для открытого ключа RSA.
        priv_key_path: Путь для закрытого ключа RSA.
        enc_key_path: Путь для зашифрованного симметричного ключа.

    Raises:
        ValueError: Если len_bits не из допустимого набора.
        OSError: При ошибках записи файлов.
    """
    print("[STEP 1] Начало генерации ключей...")

    # --- Выбор длины ключа ---
    if len_bits == 64:
        print("[WARN] Алгоритм DES удален из cryptography >= 42.0. "
              "Используется 3DES с ключом 128 бит (16 байт).")
        key_len_bytes = 16
        algo_name = "3DES (2-key, эмуляция 64-bit)"
    elif len_bits == 128:
        key_len_bytes = 16
        algo_name = "3DES (2-key)"
    elif len_bits == 192:
        key_len_bytes = 24
        algo_name = "3DES (3-key)"
    else:
        raise ValueError(
            f"Неподдерживаемая длина ключа: {len_bits}. "
            "Допустимые значения: 64, 128, 192."
        )

    # --- 1.1 Симметричный ключ ---
    sym_key = os.urandom(key_len_bytes)
    print(f"[INFO] Симметричный ключ ({algo_name}) сгенерирован. "
          f"Длина: {len(sym_key) * 8} бит.")

    # --- 1.2 Пара ключей RSA ---
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        print("[INFO] Ключи RSA (2048 бит, e=65537) сгенерированы.")
    except Exception as e:
        print(f"[ERROR] Ошибка генерации RSA: {e}")
        raise

    # --- 1.3 Сериализация закрытого ключа ---
    try:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        save_bin_data(private_pem, priv_key_path)
    except Exception as e:
        print(f"[ERROR] Ошибка сериализации закрытого ключа: {e}")
        raise

    # --- 1.3 Сериализация открытого ключа ---
    try:
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        save_bin_data(public_pem, pub_key_path)
    except Exception as e:
        print(f"[ERROR] Ошибка сериализации открытого ключа: {e}")
        raise

    # --- 1.4 Шифрование симметричного ключа RSA-OAEP ---
    try:
        encrypted_sym_key = public_key.encrypt(
            sym_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        save_bin_data(encrypted_sym_key, enc_key_path)
    except Exception as e:
        print(f"[ERROR] Ошибка шифрования симметричного ключа: {e}")
        raise

    print("[STEP 1] Генерация ключей завершена успешно.\n")