from file_utils import read_bytes, write_bytes
from asymmetric import load_symmetric_key
from symmetric import decrypt_text


def decrypt(path_cipher_text: str, path_secret_key: str,
            path_symmetric_key: str, path_original_text: str) -> None:
    """Функция расшифровки данных гибридной системой. Сначала загружается закрытый ключ,
    с его помощью извлекается симметричный ключ Camellia, и уже этим ключом расшифровывается файл.

    Args:
        path_cipher_text:   Путь к зашифрованному файлу.
        path_secret_key:    Путь к закрытому RSA-ключу для расшифровки симметричного ключа.
        path_symmetric_key: Путь к файлу зашифрованного симметричного ключа Camellia.
        path_original_text: Путь для сохранения расшифрованного файла.
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
        print(f"Расшифровка файла {path_cipher_text}.")
        data = read_bytes(path_cipher_text)
        plaintext = decrypt_text(data, symmetric_key)
        write_bytes(path_original_text, plaintext)
        print(f"Файл расшифрован и сохранён: {path_original_text}.")
    except FileNotFoundError:
        print(f"Зашифрованный файл не найден: {path_cipher_text}")
        return
    except OSError as e:
        print(f"Ошибка при чтении или записи файла: {e}")
        return
    except Exception as e:
        print(f"Не удалось расшифровать файл: {e}")
        return

    print("Готово.")