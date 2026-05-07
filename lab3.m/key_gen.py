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

    :param enc_sym_key_path: путь для зашифрованного симм. ключа
    :param public_key_path: путь для открытого RSA-ключа
    :param private_key_path: путь для закрытого RSA-ключа
    """
    try:
        print("[РЕЖИМ] Генерация ключей гибридной системы")

        print("[ШАГ 1.1] Генерация симметричного ключа IDEA...")
        idea_key = generate_idea_key()
        print("         [OK]\n")

        print("[ШАГ 1.2] Генерация пары RSA-ключей...")
        private_key, public_key = generate_rsa_keys()
        print("         [OK]\n")

        print("[ШАГ 1.3] Сериализация RSA-ключей...")
        serialize_public_key(public_key, public_key_path)
        serialize_private_key(private_key, private_key_path)
        print("         [OK]\n")

        print("[ШАГ 1.4] Шифрование ключа IDEA открытым RSA-ключом...")
        encrypted_key = rsa_encrypt(idea_key, public_key)
        save_bytes(encrypted_key, enc_sym_key_path)
        print(f"         Зашифрованный ключ сохранён: {enc_sym_key_path}")
        print("         [OK]\n")

        print("[ГОТОВО] Ключи успешно сгенерированы!")
    except Exception as e:
        print(f"[ОШИБКА] Генерация ключей не удалась: {e}")
        raise