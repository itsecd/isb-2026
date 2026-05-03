"""Гибридная криптосистема: RSA (для передачи ключа) + ChaCha20 (для шифрования данных)"""
from symmetric_crypto import generate_symmetric_key, generate_nonce, encrypt_symmetric, decrypt_symmetric
from asymmetric_crypto import generate_rsa_keypair, encrypt_asymmetric, decrypt_asymmetric
from key_manager import (
    save_symmetric_key_to_file, save_nonce_to_file, save_encrypted_data_to_file,
    save_public_key_to_file, save_private_key_to_file,
    load_private_key_from_file, load_nonce_from_file, load_encrypted_data_from_file
)
from file_utils import write_binary_file, read_binary_file, read_text_file


# ==================== Высокоуровневые операции ====================

def generate_keys(symmetric_key_path: str,
                  nonce_path: str,
                  encrypted_symmetric_key_path: str,
                  public_key_path: str,
                  private_key_path: str):
    """Задание 1: Генерация ключей гибридной системы"""
    print("\nРЕЖИМ ГЕНЕРАЦИИ КЛЮЧЕЙ\n")

    try:
        # 1. Генерация симметричного ключа и nonce
        print("1. Генерация симметричного ключа (ChaCha20, 256 бит)...")
        sym_key = generate_symmetric_key()
        print(f"   Сгенерирован ключ: {sym_key.hex()[:32]}...")

        print("2. Генерация nonce (128 бит)...")
        nonce = generate_nonce()
        print(f"   Сгенерирован nonce: {nonce.hex()}")

        # 2. Генерация RSA-ключей
        print("3. Генерация пары RSA-ключей (2048 бит)...")
        private_key, public_key = generate_rsa_keypair()
        print("   RSA-ключи сгенерированы")

        # 3. Шифрование симметричного ключа публичным ключом RSA
        print("4. Шифрование симметричного ключа публичным ключом RSA...")
        encrypted_sym_key = encrypt_asymmetric(sym_key, public_key)
        print(f"   Зашифрованный ключ (длина: {len(encrypted_sym_key)} байт)")

        # 4. Сохранение всех ключей
        print("5. Сохранение ключей в файлы...")
        save_symmetric_key_to_file(sym_key, symmetric_key_path)
        save_nonce_to_file(nonce, nonce_path)
        save_encrypted_data_to_file(encrypted_sym_key, encrypted_symmetric_key_path)
        save_public_key_to_file(public_key, public_key_path)
        save_private_key_to_file(private_key, private_key_path)

        print("\n[УСПЕХ] Генерация ключей завершена!\n")
    except Exception as e:
        print(f"\n[ОШИБКА] Генерация ключей не удалась: {e}\n")
        raise


def encrypt_data(initial_file_path: str,
                 encrypted_file_path: str,
                 encrypted_symmetric_key_path: str,
                 private_key_path: str,
                 nonce_path: str):
    """Задание 2: Шифрование данных гибридной системой"""
    print("\nРЕЖИМ ШИФРОВАНИЯ ДАННЫХ\n")

    try:
        # 1. Загрузка приватного ключа RSA
        print("1. Загрузка приватного ключа RSA...")
        private_key = load_private_key_from_file(private_key_path)

        # 2. Загрузка зашифрованного симметричного ключа и расшифровка
        print("2. Загрузка и расшифровка симметричного ключа...")
        encrypted_sym_key = load_encrypted_data_from_file(encrypted_symmetric_key_path)
        sym_key = decrypt_asymmetric(encrypted_sym_key, private_key)
        print(f"Расшифрованный симметричный ключ: {sym_key.hex()[:32]}...")

        # 3. Загрузка nonce
        print("3. Загрузка nonce...")
        nonce = load_nonce_from_file(nonce_path)

        # 4. Чтение исходного файла
        print(f"4. Чтение исходного файла: {initial_file_path}")
        plaintext = read_text_file(initial_file_path)
        print(f"Размер исходных данных: {len(plaintext)} байт")

        # 5. Шифрование ChaCha20
        print("5. Шифрование данных с помощью ChaCha20...")
        ciphertext = encrypt_symmetric(plaintext, sym_key, nonce)
        print(f"Размер зашифрованных данных: {len(ciphertext)} байт")

        # 6. Сохранение зашифрованного файла
        print(f"6. Сохранение зашифрованного файла: {encrypted_file_path}")
        write_binary_file(encrypted_file_path, ciphertext)

        print("\n[УСПЕХ] Шифрование данных завершено!\n")
    except Exception as e:
        print(f"\n[ОШИБКА] Шифрование данных не удалось: {e}\n")
        raise


def decrypt_data(encrypted_file_path: str,
                 decrypted_file_path: str,
                 encrypted_symmetric_key_path: str,
                 private_key_path: str,
                 nonce_path: str):
    """Задание 3: Дешифрование данных гибридной системой"""
    print("\nРЕЖИМ ДЕШИФРОВАНИЯ ДАННЫХ\n")

    try:
        print("1. Загрузка приватного ключа RSA...")
        private_key = load_private_key_from_file(private_key_path)

        print("2. Загрузка и расшифровка симметричного ключа...")
        encrypted_sym_key = load_encrypted_data_from_file(encrypted_symmetric_key_path)
        sym_key = decrypt_asymmetric(encrypted_sym_key, private_key)
        print(f"Расшифрованный симметричный ключ: {sym_key.hex()[:32]}...")

        print("3. Загрузка nonce...")
        nonce = load_nonce_from_file(nonce_path)

        print(f"4. Чтение зашифрованного файла: {encrypted_file_path}")
        ciphertext = read_binary_file(encrypted_file_path)
        print(f"Размер зашифрованных данных: {len(ciphertext)} байт")

        print("5. Расшифрование данных с помощью ChaCha20...")
        plaintext = decrypt_symmetric(ciphertext, sym_key, nonce)
        print(f"Размер расшифрованных данных: {len(plaintext)} байт")

        print(f"6. Сохранение расшифрованного файла: {decrypted_file_path}")
        write_binary_file(decrypted_file_path, plaintext)

        print("\n[УСПЕХ] Дешифрование данных завершено!\n")
    except Exception as e:
        print(f"\n[ОШИБКА] Дешифрование данных не удалось: {e}\n")
        raise