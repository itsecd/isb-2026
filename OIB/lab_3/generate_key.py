from file_utils import write_bytes
from asymmetric import generate_rsa_keys, serialize_public_key, serialize_private_key, encrypt_with_public_key
from symmetric import generate_symmetric_key


def generate_key(path_symmetric_key: str, path_public_key: str, path_secret_key: str,
                 key_bits: int = None) -> None:
    """Функция генерации ключей гибридной системы.
    Сначала создаётся симметричный ключ Camellia, затем пара RSA-ключей.
    Args:
        path_symmetric_key: Путь для сохранения зашифрованного симметричного ключа Camellia.
        path_public_key: Путь для сохранения открытого RSA-ключа.
        path_secret_key: Путь для сохранения закрытого RSA-ключа.
        key_bits: Длина симметричного ключа в битах (128, 192 или 256).
    """

    try:
        print("Генерация симметричного ключа Camellia.")
        symmetric_key = generate_symmetric_key(key_bits)
        print(f"Симметричный ключ сгенерирован ({key_bits} бит).")
    except ValueError as e:
        print(f"Неверная длина ключа: {e}")
        return

    try:
        print("Генерация пары RSA-ключей.")
        private_key, public_key = generate_rsa_keys()
        print("RSA-ключи сгенерированы.")
    except Exception as e:
        print(f"Не удалось сгенерировать RSA-ключи: {e}")
        return

    try:
        print("Сохранение ключей на диск.")
        serialize_public_key(public_key, path_public_key)
        serialize_private_key(private_key, path_secret_key)
        print(f"Открытый ключ сохранён: {path_public_key}.")
        print(f"Закрытый ключ сохранён: {path_secret_key}.")
    except OSError as e:
        print(f"Не удалось сохранить RSA-ключи, проверьте пути: {e}")
        return

    try:
        print("Шифрование симметричного ключа открытым RSA-ключом.")
        encrypted_sym_key = encrypt_with_public_key(symmetric_key, public_key)
        write_bytes(path_symmetric_key, encrypted_sym_key)
        print(f"Зашифрованный симметричный ключ сохранён: {path_symmetric_key}.")
    except OSError as e:
        print(f"Не удалось сохранить симметричный ключ: {e}")
        return

    print("Готово.")