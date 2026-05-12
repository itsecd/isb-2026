from file_utils import read_bytes, write_bytes
from asymmetric import load_symmetric_key
from symmetric import encrypt_text


def encrypt(path_original_text: str, path_secret_key: str,
            path_symmetric_key: str, path_cipher_text: str) -> None:
    """Функция шифрования данных гибридной системой. Сначала загружает закрытый RSA-ключ
    и с его помощью расшифровывает симметричный ключ Camellia. Затем этим симметричным
    ключом шифруется сам файл.

    Args:
        path_original_text: Путь к исходному файлу, который нужно зашифровать.
        path_secret_key: Путь к закрытому RSA-ключу для расшифровки симметричного ключа.
        path_symmetric_key: Путь к файлу зашифрованного симметричного ключа Camellia.
        path_cipher_text: Путь для сохранения зашифрованного файла.
    """

    try:
        symmetric_key = load_symmetric_key(path_secret_key, path_symmetric_key)
    except FileNotFoundError as e:
        print(f"Файл ключа не найден: {e.filename}")
        return
    except Exception as e:
        print(f"Не удалось получить симметричный ключ: {e}")
        return

    try:
        print(f"Шифрование файла {path_original_text}.")
        text = read_bytes(path_original_text)
        c_text = encrypt_text(text, symmetric_key)
        write_bytes(path_cipher_text, c_text)
        print(f"Файл зашифрован и сохранён: {path_cipher_text}.")
    except FileNotFoundError:
        print(f"Исходный файл не найден: {path_original_text}")
        return
    except OSError as e:
        print(f"Ошибка при чтении или записи файла: {e}")
        return

    print("Готово.")