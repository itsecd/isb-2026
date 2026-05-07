from rsa_module import load_private_key, rsa_decrypt
from idea_module import idea_decrypt
from file_utils import load_bytes, save_bytes


def decrypt_file(input_path: str,
                 private_key_path: str,
                 enc_sym_key_path: str,
                 output_path: str) -> None:
    """
    Дешифрование данных гибридной системой.

    :param input_path: путь к зашифрованному файлу
    :param private_key_path: путь к закрытому RSA-ключу
    :param enc_sym_key_path: путь к зашифрованному симм. ключу
    :param output_path: путь для сохранения расшифрованного файла
    """
    try:
        print("[РЕЖИМ] Дешифрование данных гибридной системой")

        print("[ШАГ 3.1] Расшифровка симметричного ключа IDEA...")
        private_key = load_private_key(private_key_path)
        encrypted_key = load_bytes(enc_sym_key_path)
        idea_key = rsa_decrypt(encrypted_key, private_key)
        print(f"         Ключ IDEA расшифрован: {idea_key.hex()[:32]}...")
        print("         [OK]\n")

        print(f"[ШАГ 3.2] Расшифровка файла: {input_path}")
        ciphertext = load_bytes(input_path)
        plaintext = idea_decrypt(ciphertext, idea_key)
        save_bytes(plaintext, output_path)
        print(f"         Файл расшифрован и сохранён: {output_path}")
        print("         [OK]\n")

        print("[ГОТОВО] Файл успешно расшифрован!")
    except Exception as e:
        print(f"[ОШИБКА] Дешифрование не удалось: {e}")
        raise