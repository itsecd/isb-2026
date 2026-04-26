"""
Модуль для шифрования/дешифрования
с использованием ключей, переданных в командной строке.
"""

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from rsa_module import rsa_decrypt
from idea_module import idea_encrypt, idea_decrypt
from file_utils import load_bytes, save_bytes


def encrypt_custom(input_path: str,
                   private_key_pem: str,
                   enc_sym_key_hex: str,
                   output_path: str) -> None:
    """
    Шифрование файла со своими ключами.

    """
    print("[РЕЖИМ] Шифрование со своими ключами")

    # Загружаем приватный RSA-ключ из PEM-строки
    print("[1/3] Загрузка приватного RSA-ключа...")
    private_key = load_pem_private_key(
        private_key_pem.encode("utf-8"),
        password=None,
    )
    print("         [OK]")

    # Расшифровываем симметричный ключ из HEX
    print("[2/3] Расшифровка симметричного ключа IDEA...")
    encrypted_key = bytes.fromhex(enc_sym_key_hex)
    idea_key = rsa_decrypt(encrypted_key, private_key)
    print(f"         [OK] Ключ: {idea_key.hex()[:32]}...")

    # Шифруем файл
    print(f"[3/3] Шифрование файла: {input_path}")
    plaintext = load_bytes(input_path)
    ciphertext = idea_encrypt(plaintext, idea_key)
    save_bytes(ciphertext, output_path)
    print(f"         Сохранено: {output_path}\n")

    print("[ГОТОВО] Файл зашифрован своими ключами!")


def decrypt_custom(input_path: str,
                   private_key_pem: str,
                   enc_sym_key_hex: str,
                   output_path: str) -> None:
    """
    Дешифрование файла со своими ключами.

    """
    print("[РЕЖИМ] Дешифрование со своими ключами")

    print("[1/3] Загрузка приватного RSA-ключа...")
    private_key = load_pem_private_key(
        private_key_pem.encode("utf-8"),
        password=None,
    )
    print("         [OK]")

    print("[2/3] Расшифровка симметричного ключа IDEA...")
    encrypted_key = bytes.fromhex(enc_sym_key_hex)
    idea_key = rsa_decrypt(encrypted_key, private_key)
    print(f"         [OK] Ключ: {idea_key.hex()[:32]}...")

    print(f"[3/3] Расшифрование файла: {input_path}")
    ciphertext = load_bytes(input_path)
    plaintext = idea_decrypt(ciphertext, idea_key)
    save_bytes(plaintext, output_path)
    print(f"         Сохранено: {output_path}\n")

    print("[ГОТОВО] Файл расшифрован своими ключами!")