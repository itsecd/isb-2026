#!/usr/bin/env python3
"""
Утилиты для гибридной криптосистемы: AES-CBC и RSA-OAEP.
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend


def generate_aes_key(key_size_bits: int) -> bytes:
    """
    Генерирует случайный ключ AES заданной длины.

    :param key_size_bits: длина ключа в битах (128, 192 или 256)
    :return: сгенерированный ключ в виде байтов
    :raises ValueError: если указана недопустимая длина ключа
    """
    if key_size_bits not in (128, 192, 256):
        raise ValueError("AES key size must be 128, 192 or 256 bits")
    return os.urandom(key_size_bits // 8)


def encrypt_file_aes(input_path: str, key: bytes, output_path: str) -> None:
    """
    Шифрует файл алгоритмом AES в режиме CBC с PKCS7-паддингом.
    Случайный инициализирующий вектор (IV) записывается в начало выходного файла.

    :param input_path: путь к исходному (открытому) файлу
    :param key: симметричный ключ AES (16, 24 или 32 байта)
    :param output_path: путь для сохранения зашифрованного файла
    :return: None
    """
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        fout.write(iv)
        while chunk := fin.read(64 * 1024):
            padded = padder.update(chunk)
            if padded:
                fout.write(encryptor.update(padded))
        final_padded = padder.finalize()
        if final_padded:
            fout.write(encryptor.update(final_padded))
        fout.write(encryptor.finalize())


def decrypt_file_aes(input_path: str, key: bytes, output_path: str) -> None:
    """
    Расшифровывает файл, зашифрованный функцией encrypt_file_aes().
    IV считывается из первых 16 байт входного файла.

    :param input_path: путь к зашифрованному файлу
    :param key: симметричный ключ AES (16, 24 или 32 байта)
    :param output_path: путь для сохранения расшифрованного файла
    :return: None
    :raises ValueError: если входной файл слишком короткий (не содержит IV)
    """
    with open(input_path, 'rb') as fin:
        iv = fin.read(16)
        if len(iv) != 16:
            raise ValueError("Encrypted file too short: missing IV")
        ciphertext = fin.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain = unpadder.update(padded_plain) + unpadder.finalize()

    with open(output_path, 'wb') as fout:
        fout.write(plain)


def generate_rsa_keypair():
    """
    Генерирует пару RSA-ключей (закрытый и открытый).
    Используется публичная экспонента 65537 и размер ключа 2048 бит.

    :return: кортеж (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key, private_key.public_key()


def save_rsa_private_key(private_key, path: str) -> None:
    """
    Сохраняет закрытый RSA-ключ в файл в формате PEM (без шифрования).

    :param private_key: закрытый ключ RSA
    :param path: путь для сохранения
    :return: None
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(path, 'wb') as f:
        f.write(pem)


def load_rsa_private_key(path: str):
    """
    Загружает закрытый RSA-ключ из PEM-файла.

    :param path: путь к файлу с закрытым ключом
    :return: загруженный закрытый ключ
    :raises FileNotFoundError: если файл не найден
    """
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )


def save_rsa_public_key(public_key, path: str) -> None:
    """
    Сохраняет открытый RSA-ключ в файл в формате PEM.

    :param public_key: открытый ключ RSA
    :param path: путь для сохранения
    :return: None
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path, 'wb') as f:
        f.write(pem)


def load_rsa_public_key(path: str):
    """
    Загружает открытый RSA-ключ из PEM-файла.

    :param path: путь к файлу с открытым ключом
    :return: загруженный открытый ключ
    """
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())


def encrypt_symmetric_key_rsa(sym_key: bytes, public_key) -> bytes:
    """
    Шифрует симметричный ключ с помощью открытого RSA-ключа.
    Используется схема OAEP с хеш-функцией SHA256.

    :param sym_key: открытый симметричный ключ (байты)
    :param public_key: открытый ключ RSA
    :return: зашифрованный симметричный ключ
    """
    return public_key.encrypt(
        sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_symmetric_key_rsa(encrypted_sym_key: bytes, private_key) -> bytes:
    """
    Расшифровывает симметричный ключ с помощью закрытого RSA-ключа.

    :param encrypted_sym_key: зашифрованный симметричный ключ
    :param private_key: закрытый ключ RSA
    :return: расшифрованный симметричный ключ
    """
    return private_key.decrypt(
        encrypted_sym_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
