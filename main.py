import argparse

from rsa_crypto import (
    unwrap_key,
    wrap_key,
    make_rsa_keys,
    read_private_key,
    dump_private_key,
    dump_public_key,
)
from io_utils import load_blob, load_json, dump_blob, dump_json
from tdes_crypto import (
    decrypt_file_3des,
    encrypt_file_3des,
    make_3des_key,
)


def prompt_paths(settings: dict) -> dict:
    """
    Запрашивает у пользователя пути к ключам и обновляет настройки.

    :param settings: исходный словарь настроек
    :return: обновлённый словарь настроек
    """
    private = input(f"Путь к приватному ключу [{settings['private_key']}]: ")
    if private:
        settings["private_key"] = private

    public = input(f"Путь к публичному ключу [{settings['public_key']}]: ")
    if public:
        settings["public_key"] = public

    symmetric = input(f"Путь к симметричному ключу [{settings['symmetric_key']}]: ")
    if symmetric:
        settings["symmetric_key"] = symmetric

    return settings


def generation_mode(settings: dict, settings_path: str) -> None:
    """
    Генерирует ключи гибридной криптосистемы.

    :param settings: словарь с настройками
    :param settings_path: путь к JSON-файлу настроек
    :return: None
    """
    settings = prompt_paths(settings)
    dump_json(settings_path, settings)

    print("[1/6] Генерация ключа 3DES")
    symmetric_key = make_3des_key(settings["key_size"])

    print("[2/6] Генерация ключей RSA")
    private_key, public_key = make_rsa_keys()

    print("[3/6] Сохранение закрытого ключа RSA")
    dump_private_key(private_key, settings["private_key"])

    print("[4/6] Сохранение открытого ключа RSA")
    dump_public_key(public_key, settings["public_key"])

    print("[5/6] Шифрование ключа 3DES открытым ключом RSA")
    encrypted_key = wrap_key(symmetric_key, public_key)

    print("[6/6] Сохранение зашифрованного ключа 3DES")
    dump_blob(settings["symmetric_key"], encrypted_key)

    print("Генерация завершена")


def encryption_mode(settings: dict) -> None:
    """
    Шифрует файл гибридной криптосистемой.

    :param settings: словарь с настройками
    :return: None
    """
    print("[1/4] Загрузка закрытого ключа RSA")
    private_key = read_private_key(settings["private_key"])

    print("[2/4] Загрузка зашифрованного ключа 3DES")
    encrypted_key = load_blob(settings["symmetric_key"])

    print("[3/4] Расшифрование ключа 3DES")
    symmetric_key = unwrap_key(encrypted_key, private_key)

    print("[4/4] Шифрование файла алгоритмом 3DES")
    encrypt_file_3des(
        settings["input_file"],
        settings["encrypted_file"],
        symmetric_key,
    )

    print("Шифрование завершено")


def decryption_mode(settings: dict) -> None:
    """
    Дешифрует файл гибридной криптосистемой.

    :param settings: словарь с настройками
    :return: None
    """
    print("[1/4] Загрузка закрытого ключа RSA")
    private_key = read_private_key(settings["private_key"])

    print("[2/4] Загрузка зашифрованного ключа 3DES")
    encrypted_key = load_blob(settings["symmetric_key"])

    print("[3/4] Расшифрование ключа 3DES")
    symmetric_key = unwrap_key(encrypted_key, private_key)

    print("[4/4] Дешифрование файла алгоритмом 3DES")
    decrypt_file_3des(
        settings["encrypted_file"],
        settings["decrypted_file"],
        symmetric_key,
    )

    print("Дешифрование завершено")


def main() -> None:
    """
    Запускает выбранный режим программы.
    """
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--gen", "--generation", dest="generation")
    group.add_argument("--enc", "--encryption", dest="encryption")
    group.add_argument("--dec", "--decryption", dest="decryption")

    parser.add_argument("--private-key", dest="private_key")
    parser.add_argument("--public-key", dest="public_key")
    parser.add_argument("--symmetric-key", dest="symmetric_key")
    parser.add_argument("--key-size", dest="key_size", type=int, choices=(64, 128, 192))

    args = parser.parse_args()

    try:
        mode = (
            args.generation is not None,
            args.encryption is not None,
            args.decryption is not None,
        )
        settings_path = args.generation or args.encryption or args.decryption
        settings = load_json(settings_path)

        if args.private_key is not None:
            settings["private_key"] = args.private_key
        if args.public_key is not None:
            settings["public_key"] = args.public_key
        if args.symmetric_key is not None:
            settings["symmetric_key"] = args.symmetric_key
        if args.key_size is not None:
            settings["key_size"] = args.key_size

        if mode == (True, False, False):
            print("Режим генерации ключей")
            generation_mode(settings, settings_path)
        elif mode == (False, True, False):
            print("Режим шифрования")
            encryption_mode(settings)
        elif mode == (False, False, True):
            print("Режим дешифрования")
            decryption_mode(settings)
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
