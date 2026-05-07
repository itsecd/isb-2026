from rsa_module import load_private_key, rsa_decrypt
from idea_module import idea_encrypt
from file_utils import load_bytes, save_bytes


def encrypt_file(input_path: str,
                 private_key_path: str,
                 enc_sym_key_path: str,
                 output_path: str) -> None:
    """
    Шифрование данных гибридной системой.

    :param input_path: путь к шифруемому файлу
    :param private_key_path: путь к закрытому RSA-ключу
    :param enc_sym_key_path: путь к зашифрованному симм. ключу
    :param output_path: путь для сохранения зашифрованного файла
    """
    try:
        print("[РЕЖИМ] Шифрование данных гибридной системой")

        print("[ШАГ 2.1] Расшифровка симметричного ключа IDEA...")
        private_key = load_private_key(private_key_path)
        encrypted_key = load_bytes(enc_sym_key_path)
        idea_key = rsa_decrypt(encrypted_key, private_key)
        print(f"         Ключ IDEA расшифрован: {idea_key.hex()[:32]}...")
        print("         [OK]\n")

        print(f"[ШАГ 2.2] Шифрование файла: {input_path}")
        plaintext = load_bytes(input_path)
        ciphertext = idea_encrypt(plaintext, idea_key)
        save_bytes(ciphertext, output_path)
        print(f"         Файл зашифрован и сохранён: {output_path}")
        print("         [OK]\n")

        print("[ГОТОВО] Файл успешно зашифрован!")
    except Exception as e:
        print(f"[ОШИБКА] Шифрование не удалось: {e}")
        raise