import os
from files import save_binary, load_private_key, read_encrypted_key, read_binary
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives import hashes   
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes




def decrypt_symmetric_key(enc_key: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Дешифрование симметричного AES-ключа закрытым RSA-ключом.
    :param enc_key: зашифрованный симметричный AES-ключ
    :param private_key: закрытый RSA-ключ для дешифрования симметричного ключа
    :return: расшифрованный симметричный AES-ключ в виде байтов
    """

    padder = asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    decrypted_key = private_key.decrypt(enc_key, padder)
    return decrypted_key


def text_encrypt(text: bytes, key: bytes) -> bytes:
    """
    Шифрование данных симметричным алгоритмом AES-CBC.
    :param text: исходные данные для шифрования в виде байтов
    :param key: симметричный AES-ключ
    :return: зашифрованные данные в виде байтов; в начале результата сохраняется IV
    """

    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 128, 192, 256 bits long")
    padder = sym_padding.ANSIX923(128).padder()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_text = padder.update(text) + padder.finalize()
    ciphertext = iv + encryptor.update(padded_text) + encryptor.finalize()
    return ciphertext


def save_encrypted_text(enc_txt: bytes, path: str) -> None:
    """
    Сохранение зашифрованных данных в файл.
    :param enc_txt: зашифрованные данные в виде байтов
    :param path: путь для сохранения зашифрованных данных
    :return: не возвращается
    """

    save_binary(enc_txt, path)


def run_scenario2(txt_path: str, prv_asym_key_path: str, enc_key_path: str, enc_txt_path: str) -> None:
    """
    Запуск сценария шифрования данных.
    :param txt_path: путь к исходному текстовому файлу
    :param prv_asym_key_path: путь к закрытому RSA-ключу
    :param enc_key_path: путь к файлу с зашифрованным симметричным AES-ключом
    :param enc_txt_path: путь для сохранения зашифрованного текстового файла
    :return: не возвращается
    """

    private_key = load_private_key(prv_asym_key_path)
    enc_key = read_encrypted_key(enc_key_path)
    decrypted_key = decrypt_symmetric_key(enc_key, private_key)
    text = read_binary(txt_path)
    enc_txt = text_encrypt(text, decrypted_key)
    save_encrypted_text(enc_txt, enc_txt_path)
    print(f"Scenario 2 completed successfully. Text from {txt_path} encrypted and saved to {enc_txt_path}.")
    
