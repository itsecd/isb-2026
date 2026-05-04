from file_utils import read_bytes, write_bytes
from asymmetric import deserialize_private_key, decrypt_with_private_key
from symmetric import encrypt_text


def encrypt(path_original_text: str, path_secret_key: str,
            path_symmetric_key: str, path_cipher_text: str) -> None:
    """Функция шифрования данных гибридной системой. Сначала загружает закрытый RSA-ключ и с его помощью расшифровывает
    симметричный ключ Camellia. Затем этим симметричным ключом шифруется сам файл."""

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