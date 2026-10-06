from asymmetric import decrypt_sym_key
from file_handler import (
    load_private_key,
    read_binary_file,
    write_binary_file,
)
from symmetric import decrypt_sym


def decrypt(
        path_cipher_text: str,
        path_private_key: str,
        path_sym_key: str,
        path_dec_text: str,
) -> None:
    """
    Расшифровывает файл гибридной схемой: симметричный ключ
    восстанавливается закрытым RSA-ключом, затем файл расшифровывается Blowfish.

    :param path_cipher_text: путь к зашифрованному файлу
    :param path_private_key: путь к закрытому RSA-ключу
    :param path_sym_key: путь к зашифрованному симметричному ключу
    :param path_dec_text: путь к расшифрованному файлу
    """

    enc_sym_key = read_binary_file(path_sym_key)

    print("Загрузка закрытого RSA-ключа")
    private_key = load_private_key(path_private_key)
    print("Закрытый RSA-ключ загружен")

    print("Получение симметричного ключа")
    sym_key = decrypt_sym_key(enc_sym_key, private_key)
    print("Симметричный ключ получен")

    print("Чтение зашифрованного файла")
    data = read_binary_file(path_cipher_text)
    print("Зашифрованный файл считан")

    print("Расшифровка файла")
    iv, c_text = data[:8], data[8:]
    dec_text = decrypt_sym(iv, c_text, sym_key)
    print("Файл расшифрован")

    print("Сохранение файла")
    write_binary_file(path_dec_text, dec_text)
    print("Файл сохранён")