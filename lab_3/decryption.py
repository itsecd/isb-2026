from asymmetric import get_symmetric_key
from symmetric import decrypt_data
from utils import read_bytes, write_bytes


def decrypt(
    path_cipher_text: str,
    path_asymmetric_private_text: str,
    path_symmetric_key: str,
    path_original_text: str,
) -> None:
    """
    Расшифровывает файл с помощью алгоритма SEED.
    Симметричный ключ расшифровывается закрытым RSA ключом перед использованием.
    Первые 16 байт зашифрованного файла считаются вектором инициализации.

    Args:
        path_cipher_text: путь к зашифрованному файлу
        path_asymmetric_private_text: путь к закрытому RSA ключу
        path_symmetric_key: путь к зашифрованному симметричному ключу
        path_original_text: путь для сохранения расшифрованного файла
    """
    print(f"Получение симметричного ключа из {path_symmetric_key}:")
    symmetric_key = get_symmetric_key(path_symmetric_key, path_asymmetric_private_text)
    print("Симметричный ключ получен")

    print(f"Чтение зашифрованного файла из {path_cipher_text}:")
    data = read_bytes(path_cipher_text)
    print("Зашифрованный файл считан")

    print("Расшифровка файла:")
    iv, c_text = data[:16], data[16:]
    result = decrypt_data(iv, c_text, symmetric_key)
    print("Файл расшифрован")

    print(f"Сохранение расшифрованного файла в {path_original_text}:")
    write_bytes(path_original_text, result)
    print("Расшифровка завершена успешно")