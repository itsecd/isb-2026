from file_utils import read_bytes, write_bytes
from asymmetric import deserialize_private_key, decrypt_with_private_key
from symmetric import decrypt_text


def decrypt(path_cipher_text: str, path_secret_key: str,
            path_symmetric_key: str, path_original_text: str) -> None:
    """Функция расшифровки данных гибридной системой. Сначала загружается закрытый ключ,
    с его помощью извлекается симметричный ключ Camellia, и уже этим ключом расшифровывается файл."""

    try:
        print("Загрузка закрытого ключа.")
        private_key = deserialize_private_key(path_secret_key)
    except FileNotFoundError:
        print(f"Файл закрытого ключа не найден: {path_secret_key}")
        return
    except Exception as e:
        print(f"Не удалось загрузить закрытый ключ: {e}")
        return

    try:
        print("Расшифровка симметричного ключа.")
        encrypted_sym_key = read_bytes(path_symmetric_key)
        symmetric_key = decrypt_with_private_key(encrypted_sym_key, private_key)
        print(f"Симметричный ключ получен ({len(symmetric_key) * 8} бит).")
    except FileNotFoundError:
        print(f"Файл симметричного ключа не найден: {path_symmetric_key}")
        return
    except Exception as e:
        print(f"Не удалось расшифровать симметричный ключ: {e}")
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