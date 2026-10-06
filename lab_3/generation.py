from asymmetric import encrypt_sym_key, generate_rsa_keys
from file_handler import (
    save_private_key,
    save_public_key,
    write_binary_file,
)
from symmetric import generate_sym_key


def generate(
        path_sym_key: str,
        path_public_key: str,
        path_private_key: str,
        key_length: int = 128,
) -> None:
    """
    Генерирует ключи гибридной системы: симметричный ключ Blowfish,
    пару RSA-ключей и сохраняет их на диск.

    :param path_sym_key: путь к зашифрованному симметричному ключу
    :param path_public_key: путь к открытому RSA-ключу
    :param path_private_key: путь к закрытому RSA-ключу
    :param key_length: длина ключа Blowfish в битах
    """

    print("Генерация симметричного ключа")
    sym_key = generate_sym_key(key_length)
    print("Симметричный ключ сгенерирован")

    print("Генерация открытого и закрытого RSA-ключей")
    private_key, public_key = generate_rsa_keys()
    print("Открытый и закрытый RSA-ключи сгенерированы")

    print("Шифрование симметричного ключа открытым RSA-ключом")
    enc_sym_key = encrypt_sym_key(sym_key, public_key)
    print("Симметричный ключ зашифрован")

    print("Сохранение зашифрованного симметричного ключа")
    write_binary_file(path_sym_key, enc_sym_key)
    print("Зашифрованный симметричный ключ сохранён")

    print("Сохранение открытого RSA-ключа")
    save_public_key(path_public_key, public_key)
    print("Открытый RSA-ключ сохранён")

    print("Сохранение закрытого RSA-ключа")
    save_private_key(path_private_key, private_key)
    print("Закрытый RSA-ключ сохранён")