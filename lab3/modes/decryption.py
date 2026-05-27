from crypto.rsa_utils import load_private_key, rsa_decrypt
from crypto.sm4_utils import sm4_decrypt
from crypto.file_utils import read_binary_file, save_text_file, compare_files_content


def decryption_mode(settings):
    """
    Выполняет дешифрование файла гибридной системой.

    Args:
        settings (dict): Настройки приложения.

    Raises:
        Exception: При ошибке дешифрования.
    """

    try:
        print("[🗝] Загрузка приватного RSA ключа...")
        private_key = load_private_key(settings["private_key"])

        print("[🗝] Загрузка зашифрованного SM4 ключа...")
        encrypted_sm4_key = read_binary_file(settings["encrypted_symmetric_key"])

        print("[🗝] Расшифровка SM4 ключа...")
        sm4_key = rsa_decrypt(private_key, encrypted_sm4_key)

        print("[✉] Чтение зашифрованного файла...")
        encrypted_data = read_binary_file(settings["encrypted_file"])

        print("[✉] Дешифрование файла...")
        decrypted_text = sm4_decrypt(sm4_key, encrypted_data)
        save_text_file(settings["decrypted_file"], decrypted_text)

        print("[✔] Файл успешно расшифрован!")

    except Exception as err:
        raise Exception(f"Ошибка режима дешифрования: {err}")
