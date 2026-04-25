"""Гибридная криптосистема: RSA (для передачи ключа) + ChaCha20 (для шифрования данных)"""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import constants as const

# Симметричное шифрование (ChaCha20) 
def generate_symmetric_key() -> bytes:
    """ Генерирует случайный ключ для ChaCha20 (256 бит = 32 байта) """
    return os.urandom(const.SYMMETRIC_KEY_SIZE)


def generate_nonce() -> bytes:
    """ Генерирует случайное одноразовое число (nonce) для ChaCha20 (128 бит = 16 байт) """
    return os.urandom(const.NONCE_SIZE)


def encrypt_symmetric(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Шифрование данных с помощью ChaCha20  вернет: зашифрованные данные (ciphertext) """
    # ChaCha20 в режиме потокового шифра (без дополнительного padding)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext


def decrypt_symmetric(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Расшифрование данных с помощью ChaCha20(key: 32 байта, nonce: 16 байт) вернет: расшифрованные данные (plaintext) """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


# Асимметричное шифрование (RSA) 
def generate_rsa_keypair() -> tuple:
    """ Генерирует пару ключей RSA (приватный, публичный) вернет: (private_key, public_key) """
    private_key = rsa.generate_private_key(
        public_exponent=const.RSA_PUBLIC_EXPONENT,
        key_size=const.RSA_KEY_SIZE
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_asymmetric(data: bytes, public_key) -> bytes:
    """ Шифрование данных с помощью RSA (OAEP padding) """
    ciphertext = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return ciphertext


def decrypt_asymmetric(ciphertext: bytes, private_key) -> bytes:
    """ Дешифрование данных с помощью RSA """
    plaintext = private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return plaintext


# Сериализация / десериализация ключей 

def save_symmetric_key_to_file(key: bytes, filepath: str):
    """Сохраняет симметричный ключ в бинарный файл (сериализация)"""
    with open(filepath, 'wb') as f:
        f.write(key)
    print(f"[OK] Симметричный ключ сохранён в {filepath}")


def load_symmetric_key_from_file(filepath: str) -> bytes:
    """ Загружает симметричный ключ из бинарного файла (десериализация) """
    with open(filepath, 'rb') as f:
        key = f.read()
    if len(key) != const.SYMMETRIC_KEY_SIZE:
        raise ValueError(f"Неверный размер ключа: ожидается {const.SYMMETRIC_KEY_SIZE} байт")
    print(f"[OK] Симметричный ключ загружен из {filepath}")
    return key


def save_nonce_to_file(nonce: bytes, filepath: str):
    """Сохраняет nonce в бинарный файл (сериализация)"""
    with open(filepath, 'wb') as f:
        f.write(nonce)
    print(f"[OK] Nonce сохранён в {filepath}")


def load_nonce_from_file(filepath: str) -> bytes:
    """Загружает nonce из бинарного файла (десериализация) """
    with open(filepath, 'rb') as f:
        nonce = f.read()
    if len(nonce) != const.NONCE_SIZE:
        raise ValueError(f"Неверный размер nonce: ожидается {const.NONCE_SIZE} байт")
    print(f"[OK] Nonce загружен из {filepath}")
    return nonce


def save_public_key_to_file(public_key, filepath: str):
    """Сохраняет публичный ключ RSA в PEM-файл"""
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(filepath, 'wb') as f:
        f.write(pem)
    print(f"[OK] Публичный ключ RSA сохранён в {filepath}")


def save_private_key_to_file(private_key, filepath: str):
    """Сохраняет приватный ключ RSA в PEM-файл (без шифрования)"""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filepath, 'wb') as f:
        f.write(pem)
    print(f"[OK] Приватный ключ RSA сохранён в {filepath}")


def load_public_key_from_file(filepath: str):
    """ Загружает публичный ключ RSA из PEM-файла"""
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    public_key = serialization.load_pem_public_key(pem_data)
    print(f"[OK] Публичный ключ RSA загружен из {filepath}")
    return public_key


def load_private_key_from_file(filepath: str):
    """Загружает приватный ключ RSA из PEM-файла"""
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    private_key = serialization.load_pem_private_key(pem_data, password=None)
    print(f"[OK] Приватный ключ RSA загружен из {filepath}")
    return private_key


# Высокоуровневые операции

def generate_keys(symmetric_key_path: str,
                  nonce_path: str,
                  encrypted_symmetric_key_path: str,
                  public_key_path: str,
                  private_key_path: str):
    """Задание 1: Генерация ключей гибридной системы"""
    print("\nРЕЖИМ ГЕНЕРАЦИИ КЛЮЧЕЙ\n")

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


def encrypt_data(initial_file_path: str,
                 encrypted_file_path: str,
                 encrypted_symmetric_key_path: str,
                 private_key_path: str,
                 nonce_path: str):        
    """Задание 2: Шифрование данных гибридной системой"""
    print("\nРЕЖИМ ШИФРОВАНИЯ ДАННЫХ\n")

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
    with open(initial_file_path, 'rb') as f:
        plaintext = f.read()
    print(f"Размер исходных данных: {len(plaintext)} байт")

    # 5. Шифрование ChaCha20
    print("5. Шифрование данных с помощью ChaCha20...")
    ciphertext = encrypt_symmetric(plaintext, sym_key, nonce)
    print(f"Размер зашифрованных данных: {len(ciphertext)} байт")

    # 6. Сохранение зашифрованного файла
    print(f"6. Сохранение зашифрованного файла: {encrypted_file_path}")
    with open(encrypted_file_path, 'wb') as f:
        f.write(ciphertext)

    print("\n[УСПЕХ] Шифрование данных завершено!\n")

def decrypt_data(encrypted_file_path: str,
                 decrypted_file_path: str,
                 encrypted_symmetric_key_path: str,
                 private_key_path: str,
                 nonce_path: str):          # ← ДОБАВЛЕН ПАРАМЕТР nonce_path
    """Задание 3: Дешифрование данных гибридной системой"""
    print("\nРЕЖИМ ДЕШИФРОВАНИЯ ДАННЫХ\n")

    print("1. Загрузка приватного ключа RSA...")
    private_key = load_private_key_from_file(private_key_path)

    print("2. Загрузка и расшифровка симметричного ключа...")
    encrypted_sym_key = load_encrypted_data_from_file(encrypted_symmetric_key_path)
    sym_key = decrypt_asymmetric(encrypted_sym_key, private_key)
    print(f"Расшифрованный симметричный ключ: {sym_key.hex()[:32]}...")

    print("3. Загрузка nonce...")
    nonce = load_nonce_from_file(nonce_path)

    print(f"4. Чтение зашифрованного файла: {encrypted_file_path}")
    with open(encrypted_file_path, 'rb') as f:
        ciphertext = f.read()
    print(f"Размер зашифрованных данных: {len(ciphertext)} байт")

    print("5. Расшифрование данных с помощью ChaCha20...")
    plaintext = decrypt_symmetric(ciphertext, sym_key, nonce)
    print(f"Размер расшифрованных данных: {len(plaintext)} байт")

    print(f"6. Сохранение расшифрованного файла: {decrypted_file_path}")
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    print("\n[УСПЕХ] Дешифрование данных завершено!\n")


def save_encrypted_data_to_file(data: bytes, filepath: str):
    """Сохраняет зашифрованные данные (RSA-шифротекст) в файл"""
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f"[OK] Зашифрованные данные сохранены в {filepath}")


def load_encrypted_data_from_file(filepath: str) -> bytes:
    """Загружает зашифрованные данные из файла"""
    with open(filepath, 'rb') as f:
        data = f.read()
    print(f"[OK] Зашифрованные данные загружены из {filepath}")
    return data