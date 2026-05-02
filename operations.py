import os
import sys
from generator_key import creater_symmetric_key, creater_asymmetrical_key
from load_and_save_key import (
    serialize_asymmetric_keys,
    save_symmetric_key,
    load_private_key,
    read_file,
    write_text_file,
    read_encrypted_text,
)
from asymmetrical import encrypt_symmetric_key, decrypt_symmetric_key
from symmetrical import encrypt_AES, decrypt_aes_cbc


def run_generation(settings: dict, key_bits: int) -> None:
    """Генерирует и сохраняет симметричные и асимметричные ключи."""
    print("ЗАПУСК РЕЖИМА ГЕНЕРАЦИИ КЛЮЧЕЙ ")
    print("Генерация симметричного ключа (AES)")
    sym_key = creater_symmetric_key(key_bits)

    print("Генерация пары RSA ключей")
    priv_key, pub_key = creater_asymmetrical_key()

    print("Сериализация и сохранение асимметричных ключей")
    serialize_asymmetric_keys(
        priv_key, pub_key, settings["public_key"], settings["secret_key"]
    )

    print("Шифрование симметричного ключа открытым RSA ключом и сохранение")
    enc_sym_key = encrypt_symmetric_key(pub_key, sym_key)
    save_symmetric_key(enc_sym_key, settings["symmetric_key"])

    print("ГЕНЕРАЦИЯ КЛЮЧЕЙ УСПЕШНО ЗАВЕРШЕНА\n")


def run_encryption(settings: dict) -> None:
    """Шифрует исходный файл с использованием гибридной системы."""
    print("ЗАПУСК РЕЖИМА ШИФРОВАНИЯ")
    if not os.path.exists(settings["initial_file"]):
        print(f"Ошибка: Исходный файл '{settings['initial_file']}' не найден!")
        sys.exit(1)

    print("Загрузка закрытого ключа RSA и расшифровка симметричного ключа")
    priv_key = load_private_key(settings["secret_key"])
    enc_sym_key_data = read_encrypted_text(settings["symmetric_key"])
    sym_key = decrypt_symmetric_key(priv_key, enc_sym_key_data)

    print("Чтение текста, шифрование AES и сохранение")
    plaintext = read_file(settings["initial_file"])
    encrypted_data = encrypt_AES(plaintext, sym_key)

    with open(settings["encrypted_file"], "wb") as f:
        f.write(encrypted_data)

    print("ШИФРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО\n")


def run_decryption(settings: dict) -> None:
    """Расшифровывает файл с использованием гибридной системы."""
    print("ЗАПУСК РЕЖИМА ДЕШИФРОВАНИЯ")
    if not os.path.exists(settings["encrypted_file"]):
        print(f"Ошибка: Зашифрованный файл '{settings['encrypted_file']}' не найден!")
        sys.exit(1)

    print("Загрузка закрытого ключа RSA и расшифровка симметричного ключа")
    priv_key = load_private_key(settings["secret_key"])
    enc_sym_key_data = read_encrypted_text(settings["symmetric_key"])
    sym_key = decrypt_symmetric_key(priv_key, enc_sym_key_data)

    print("Чтение зашифрованных данных, расшифровка AES и сохранение")
    encrypted_data = read_encrypted_text(settings["encrypted_file"])
    decrypted_text = decrypt_aes_cbc(encrypted_data, sym_key)

    write_text_file(decrypted_text, settings["decrypted_file"])

    print("ДЕШИФРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО\n")
