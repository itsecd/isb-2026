from asymmetric import get_symmetric_key
from symmetric import encrypt_data
from utils import read_bytes, write_bytes


def encrypt(
    path_original_text: str,
    path_asymmetric_private_text: str,
    path_symmetric_key: str,
    path_cipher_text: str,
) -> None:
    """
    Шифрует файл с помощью алгоритма SEED.
    Симметричный ключ расшифровывается закрытым RSA ключом перед использованием.
    Результат сохраняется вместе с вектором инициализации.

    Args:
        path_original_text: путь к исходному файлу для шифрования
        path_asymmetric_private_text: путь к закрытому RSA ключу
        path_symmetric_key: путь к зашифрованному симметричному ключу
        path_cipher_text: путь для сохранения зашифрованного файла
    """
    print(f"Получение симметричного ключа из {path_symmetric_key}:")
    symmetric_key = get_symmetric_key(path_symmetric_key, path_asymmetric_private_text)
    print("Симметричный ключ получен")

    print(f"Чтение исходного файла из {path_original_text}:")
    text = read_bytes(path_original_text)
    print("Исходный файл считан")

    print("Шифрование файла:")
    iv, c_text = encrypt_data(text, symmetric_key)
    print("Файл зашифрован")

    print(f"Сохранение зашифрованного файла в {path_cipher_text}:")
    write_bytes(path_cipher_text, iv + c_text)
    print("Шифрование завершено успешно")