from crypto.rsa_utils import load_private_key, rsa_decrypt
from crypto.sm4_utils import sm4_encrypt
from crypto.file_utils import read_binary_file, read_text_file, save_binary_file


def encryption_mode(settings):
    """
    Выполняет шифрование файла гибридной системой.

    Args:
        settings (dict): Настройки приложения.

    Raises:
        Exception: При ошибке шифрования.
    """

    try:
        print("[🗝] Загрузка приватного RSA ключа...")
        private_key = load_private_key(settings["private_key"])

        print("[🗝] Загрузка зашифрованного SM4 ключа...")
        encrypted_sm4_key = read_binary_file(settings["encrypted_symmetric_key"])

        print("[🗝] Расшифровка SM4 ключа...")
        sm4_key = rsa_decrypt(private_key, encrypted_sm4_key)

        print("[✉] Чтение исходного файла...")
        text = read_text_file(settings["initial_file"])

        print("[✉] Шифрование файла...")
        encrypted_data = sm4_encrypt(sm4_key, text)
        save_binary_file(settings["encrypted_file"], encrypted_data)

        print("[✔] Файл успешно зашифрован!")

    except Exception as err:
        raise Exception(f"Ошибка режима шифрования: {err}")