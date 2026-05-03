import json
import argparse

from symmetric_crypto import generate_symmetric_key, encrypt_file_aes, decrypt_file_aes
from asymmetric_crypto import generate_rsa_key, save_private_key, save_public_key, load_private_key, encrypt_symmetric_key, decrypt_symmetric_key, save_encrypted_symmetric_key

def load_settings(settings_path: str) -> dict[str, str]:
    """
    Загружает настройки из JSON-файла.
    """
    try:
        with open(settings_path, "r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)

        return settings

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Файл настроек не найден: {settings_path}"
        )

def generation_mode(settings: dict[str,str]) ->None:
    """
    Генерирует ключи гибридной системы.
    :param settings: словарь с путями к файлам ключей
    :return: None
    """
    print("Генерация симметричного ключа AES")
    symmetric_key = generate_symmetric_key()

    print("Генерация ключей RSA")
    private_key, public_key = generate_rsa_key()

    print("Сохранение открытого ключа RSA")
    save_public_key(public_key, settings["public_key"])
    
    print("Сохранение закрытого ключа RSA")
    save_private_key(private_key, settings["private_key"])

    print("Шифрование симметричного ключа открытым ключом RSA")
    encrypted_key = encrypt_symmetric_key(symmetric_key, public_key)

    print("Сохранение зашифрованного симметричного ключа")
    save_encrypted_symmetric_key(encrypted_key, settings["symmetric_key"])


def encryption_mode(settings: dict[str,str]) -> None:
    """
    Шифрует файл гибридной системой.
    """
    print("Загрузка закрытого ключа RSA")
    private_key = load_private_key(settings["private_key"])

    print("Загрузка зашифрованного симметричного ключа")
    with open(settings["symmetric_key"], "rb") as key_file:
        encrypted_key = key_file.read()

    print("Расшифрование симметричного ключа")
    symmetric_key = decrypt_symmetric_key(encrypted_key,private_key)

    print("Шифрование файла с помощью AES")
    encrypt_file_aes(settings["initial_file"], settings["encrypted_file"],symmetric_key)

    print("Шифрование файла завершено.")

def decryption_mode(settings: dict[str,str]) -> None:
    """
    Дешифрует файл гибридной системой.
    """
    print("Загрузка закрытого ключа RSA")
    private_key = load_private_key(settings["private_key"])

    print("Загрузка зашифрованного симметричного ключа")
    with open(settings["symmetric_key"], "rb") as key_file:
        encrypted_key = key_file.read()
    
    print("Расшифрование симметричного ключа")
    symmetric_key = decrypt_symmetric_key(encrypted_key, private_key)

    print("Дешифрование файла с помощью AES")
    decrypt_file_aes(settings["encrypted_file"], settings["decrypted_file"], symmetric_key)

    print("Дешифрование файла завершено.")

def main() -> None:
    """
    Запускает выбранный режим программы.
    """
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--gen", "--generation", dest="generation", help="Запускает режим генерации ключей")
    group.add_argument("--enc", "--encryption", dest="encryption", help="Запускает режим шифрования")
    group.add_argument("--dec", "--decryption", dest="decryption", help="Запускает режим дешифрования")
    parser.add_argument("--private-key", dest="private_key", help="Путь к пользовательскому закрытому RSA-ключу")
    parser.add_argument("--symmetric-key", dest="symmetric_key", help="Путь к пользовательскому зашифрованному симметричному ключу")

    args = parser.parse_args()

    match(args.generation is not None, args.encryption is not None, args.decryption is not None):
        case (True, False, False):
            print("Режим генерации ключей начинается")
            settings = load_settings(args.generation)
            generation_mode(settings)
        case (False, True, False):
            print("Режим шифрования начинается")
            settings = load_settings(args.encryption)
            if args.private_key is not None:
                settings["private_key"] = args.private_key
            if args.symmetric_key is not None:
                settings["symmetric_key"] = args.symmetric_key
            encryption_mode(settings)
        case (False, False, True):
            print("Режим дешифрования начинается")
            settings = load_settings(args.decryption)
            if args.private_key is not None:
                settings["private_key"] = args.private_key
            if args.symmetric_key is not None:
                settings["symmetric_key"] = args.symmetric_key
            decryption_mode(settings)
        case _:
            raise ValueError("Неизвестный режим работы программы.")
        

if __name__ == "__main__":
    main()