from asymmetric import decrypt_sym_key
from file_handler import (
    load_private_key,
    read_binary_file,
    write_binary_file,
)
from symmetric import encrypt_sym


def encrypt(
        path_original_text: str,
        path_private_key: str,
        path_sym_key: str,
        path_cipher_text: str,
) -> None:
    """
    Шифрует файл гибридной схемой: симметричный ключ восстанавливается
    закрытым RSA-ключом, затем файл шифруется Blowfish.

    :param path_original_text: путь к исходному файлу
    :param path_private_key: путь к закрытому RSA-ключу
    :param path_sym_key: путь к зашифрованному симметричному ключу
    :param path_cipher_text: путь к зашифрованному файлу
    """

    enc_sym_key = read_binary_file(path_sym_key)
    text = read_binary_file(path_original_text)

    print("Загрузка закрытого RSA-ключа")
    private_key = load_private_key(path_private_key)
    print("Закрытый RSA-ключ загружен")

    print("Получение симметричного ключа")
    sym_key = decrypt_sym_key(enc_sym_key, private_key)
    print("Симметричный ключ получен")

    print("Шифрование текста симметричным алгоритмом")
    iv, c_text = encrypt_sym(text, sym_key)
    print("Шифрование текста завершено")

    print("Сохранение зашифрованного файла")
    write_binary_file(path_cipher_text, iv + c_text)
    print("Шифрование завершено")