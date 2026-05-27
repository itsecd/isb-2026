from crypto.sm4_utils import generate_sm4_key
from crypto.rsa_utils import generate_rsa_keys, save_public_key, save_private_key, rsa_encrypt
from crypto.file_utils import save_binary_file


def key_generation_mode(settings):
    """
    Выполняет генерацию ключей гибридной криптосистемы.

    Args:
        settings (dict): Настройки приложения.

    Raises:
        Exception: При ошибке генерации или сохранения ключей.
    """

    try:
        print("[🗝] Генерация SM4 ключа...")
        sm4_key = generate_sm4_key()

        print("[🗝] Генерация RSA ключей...")
        private_key, public_key = generate_rsa_keys()

        print("[🗝🗝] Сохранение RSA ключей...")
        save_public_key(public_key,settings["public_key"])
        save_private_key(private_key,settings["private_key"])

        print("[🗝] Шифрование SM4 ключа...")
        encrypted_sm4_key = rsa_encrypt(public_key, sm4_key)

        save_binary_file(settings["encrypted_symmetric_key"], encrypted_sm4_key)

        print("[🗝🗝] Генерация ключей завершена!")

    except Exception as err:
        raise Exception(f"Ошибка режима генерации ключей: {err}")