"""
Три сценария работы гибридной криптосистемы:
  1. Генерация ключей
  2. Шифрование файла
  3. Дешифрование файла
"""

import crypto.symmetric as symmetric
import crypto.asymmetric as asymmetric
import crypto.key_serialization as key_serialization
from crypto.file_utils import log, save_bytes, load_bytes


def generate_keys(cfg: dict) -> None:
    """
    Сценарий 1: Генерация ключей гибридной системы.
    
    Args:
        cfg: Словарь конфигурации с путями для сохранения ключей.

    Шаги:
    1.1 Генерация симметричного ключа SM4.
    1.2 Генерация пары RSA-ключей.
    1.3 Сериализация RSA-ключей в PEM-файлы.
    1.4 Шифрование симметричного ключа открытым RSA-ключом и сохранение.
    """
    # Загрузиув параметры криптографии из конфигурации
    if 'crypto' in cfg:
        symmetric.set_parameters(
            cfg['crypto'].get('sm4_block_size_bits', 128),
            cfg['crypto'].get('sm4_key_size_bytes', 16),
            cfg['crypto'].get('sm4_iv_size_bytes', 16),
        )
        asymmetric.set_parameters(
            cfg['crypto'].get('rsa_key_size', 2048),
            cfg['crypto'].get('rsa_public_exponent', 65537),
        )
    
    log("Шаг 1.1 — Генерация симметричного ключа SM4 (128 бит)...")
    sym_key = symmetric.generate_symmetric_key()

    log("Шаг 1.2 — Генерация пары RSA-2048 ключей...")
    private_key, public_key = asymmetric.generate_rsa_keys()

    log(f"Шаг 1.3 — Сохранение открытого ключа → {cfg['public_key']}")
    key_serialization.save_public_key(public_key, cfg["public_key"])

    log(f"Шаг 1.3 — Сохранение закрытого ключа → {cfg['secret_key']}")
    key_serialization.save_private_key(private_key, cfg["secret_key"])

    log("Шаг 1.4 — Шифрование симметричного ключа открытым RSA-ключом...")
    encrypted_sym_key = asymmetric.encrypt(sym_key, public_key)

    log(f"Шаг 1.4 — Сохранение зашифрованного симметричного ключа → {cfg['symmetric_key']}")
    save_bytes(encrypted_sym_key, cfg["symmetric_key"])

    log("✓ Генерация ключей завершена.")


def encrypt_file(cfg: dict) -> None:
    """
    Сценарий 2: Шифрование данных гибридной системой.
    
    Args:
        cfg: Словарь конфигурации с путями ключей и файлов.

    Шаги:
    2.1 Расшифровка симметричного ключа закрытым RSA-ключом.
    2.2 Шифрование файла симметричным алгоритмом SM4.
    """
    log(f"Загрузка закрытого RSA-ключа из {cfg['secret_key']}...")
    private_key = key_serialization.load_private_key(cfg["secret_key"])

    log(f"Загрузка зашифрованного симметричного ключа из {cfg['symmetric_key']}...")
    encrypted_sym_key = load_bytes(cfg["symmetric_key"])

    log("Шаг 2.1 — Расшифровка симметричного ключа...")
    sym_key = asymmetric.decrypt(encrypted_sym_key, private_key)

    log(f"Чтение исходного файла: {cfg['initial_file']}")
    plaintext = load_bytes(cfg["initial_file"])

    log("Шаг 2.2 — Шифрование файла алгоритмом SM4-CBC...")
    ciphertext = symmetric.encrypt(plaintext, sym_key)

    log(f"Шаг 2.2 — Сохранение зашифрованного файла → {cfg['encrypted_file']}")
    save_bytes(ciphertext, cfg["encrypted_file"])

    log("✓ Шифрование завершено.")


def decrypt_file(cfg: dict) -> None:
    """
    Сценарий 3: Дешифрование данных гибридной системой.
    
    Args:
        cfg: Словарь конфигурации с путями ключей и файлов.

    Шаги:
    3.1 Расшифровка симметричного ключа закрытым RSA-ключом.
    3.2 Расшифровка файла симметричным алгоритмом SM4.
    """
    log(f"Загрузка закрытого RSA-ключа из {cfg['secret_key']}...")
    private_key = key_serialization.load_private_key(cfg["secret_key"])

    log(f"Загрузка зашифрованного симметричного ключа из {cfg['symmetric_key']}...")
    encrypted_sym_key = load_bytes(cfg["symmetric_key"])

    log("Шаг 3.1 — Расшифровка симметричного ключа...")
    sym_key = asymmetric.decrypt(encrypted_sym_key, private_key)

    log(f"Чтение зашифрованного файла: {cfg['encrypted_file']}")
    ciphertext = load_bytes(cfg["encrypted_file"])

    log("Шаг 3.2 — Расшифровка файла алгоритмом SM4-CBC...")
    plaintext = symmetric.decrypt(ciphertext, sym_key)

    log(f"Шаг 3.2 — Сохранение расшифрованного файла → {cfg['decrypted_file']}")
    save_bytes(plaintext, cfg["decrypted_file"])

    log("✓ Дешифрование завершено.")
