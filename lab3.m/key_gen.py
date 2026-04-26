"""
Модуль генерации ключей гибридной системы.
"""

from rsa_module import (
    generate_rsa_keys,
    serialize_public_key,
    serialize_private_key,
    rsa_encrypt,
)
from idea_module import generate_idea_key
from file_utils import save_bytes


def generate_keys(enc_sym_key_path: str,
                  public_key_path: str,
                  private_key_path: str) -> None:
    """
    Генерация ключей гибридной системы.

    """
    print("[РЕЖИМ] Генерация ключей гибридной системы")

    # 1.1. Симметричный ключ IDEA
    print("[ШАГ 1.1] Генерация симметричного ключа IDEA...")
    idea_key = generate_idea_key()
    print("         [OK]\n")

    # 1.2. Пара RSA-ключей
    print("[ШАГ 1.2] Генерация пары RSA-ключей...")
    private_key, public_key = generate_rsa_keys()
    print("         [OK]\n")

    # 1.3. Сериализация
    print("[ШАГ 1.3] Сериализация RSA-ключей...")
    serialize_public_key(public_key, public_key_path)
    serialize_private_key(private_key, private_key_path)
    print("         [OK]\n")

    # 1.4. Шифрование симм. ключа открытым RSA
    print("[ШАГ 1.4] Шифрование ключа IDEA открытым RSA-ключом...")
    encrypted_key = rsa_encrypt(idea_key, public_key)
    save_bytes(encrypted_key, enc_sym_key_path)
    print(f"         Зашифрованный ключ сохранён: {enc_sym_key_path}")
    print("         [OK]\n")

    print("[ГОТОВО] Ключи успешно сгенерированы!")