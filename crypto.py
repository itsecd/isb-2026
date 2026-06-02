"""
Модуль симметричного шифрования и дешифрования (3DES-CBC).

Перед каждой операцией восстанавливает симметричный ключ из
RSA-шифрованного контейнера. Использует паддинг ANSI X.923
согласно примерам методички.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from utils import load_bin_data, save_bin_data


ef decrypt_sym_key(priv_key_path: str, enc_key_path: str) -> bytes:
    """
    Расшифровывает симметричный ключ закрытым ключом RSA.

    Args:
        priv_key_path: Путь к закрытому ключу RSA (PEM).
        enc_key_path: Путь к зашифрованному симметричному ключу.

    Returns:
        Байты симметричного ключа.

    Raises:
        FileNotFoundError: Если файлы ключей отсутствуют.
        ValueError: Если десериализация или расшифровка не удались.
        Exception: Прочие криптографические ошибки.
    """
    private_key = _load_rsa_private_key(priv_key_path)

    sym_key = _decrypt_symmetric_key(private_key, enc_key_path)

    print(f"[INFO] Симметричный ключ расшифрован. "
          f"Длина: {len(sym_key) * 8} бит.")
    return sym_key


def _load_rsa_private_key(priv_key_path: str):
    """Загружает закрытый RSA ключ из PEM файла."""
    try:
        private_pem = load_bin_data(priv_key_path)
        private_key = serialization.load_pem_private_key(
            private_pem, password=None
        )
        return private_key
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Закрытый ключ RSA не найден: {e}")
    except ValueError as e:
        raise ValueError(f"Неверный формат закрытого ключа: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки закрытого ключа: {e}")


def _decrypt_symmetric_key(private_key, enc_key_path: str):
    """Расшифровывает симметричный ключ используя RSA-OAEP."""
    try:
        encrypted_sym_key = load_bin_data(enc_key_path)
        sym_key = private_key.decrypt(
            encrypted_sym_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return sym_key
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Зашифрованный симметричный ключ не найден: {e}")
    except ValueError as e:
        raise ValueError(f"Ошибка расшифровки симметричного ключа (неверный ключ): {e}")
    except Exception as e:
        raise RuntimeError(f"Критическая ошибка при расшифровке симметричного ключа: {e}")


def get_algo(sym_key: bytes):
    """
    Возвращает объект алгоритма на основе длины ключа.

    Поддерживает DES (8 байт, только cryptography < 42.0)
    и TripleDES (16 или 24 байта).

    Args:
        sym_key: Байты симметричного ключа.

    Returns:
        Экземпляр algorithms.DES или algorithms.TripleDES.

    Raises:
        ValueError: Если длина ключа недопустима.
    """
    if len(sym_key) == 8:
        return algorithms.DES(sym_key)
    elif len(sym_key) in (16, 24):
        return algorithms.TripleDES(sym_key)
    else:
        raise ValueError(
            f"Неверная длина симметричного ключа: {len(sym_key)} байт. "
            f"Ожидалось 8 (DES), 16 или 24 (TripleDES)."
        )


def encrypt_data(
    input_path: str,
    priv_key_path: str,
    enc_key_path: str,
    output_path: str
) -> None:
    """
    Шифрует файл гибридной системой (RSA + 3DES-CBC).

    1. Восстанавливает симметричный ключ через RSA.
    2. Применяет паддинг ANSI X.923 (блок 8 байт).
    3. Шифрует в режиме CBC со случайным IV.
    4. Сохраняет результат как [IV(8B) || Ciphertext].

    Args:
        input_path: Путь к исходному файлу.
        priv_key_path: Путь к закрытому ключу RSA.
        enc_key_path: Путь к зашифрованному симметричному ключу.
        output_path: Путь для зашифрованного результата.

    Raises:
        FileNotFoundError: Если входной файл или ключи отсутствуют.
        ValueError: При неверном ключе или данных.
        OSError: При ошибках записи.
    """
    print("[STEP 2] Начало шифрования данных...")

    # 2.1 Расшифровка симметричного ключа
    sym_key = _decrypt_sym_key(priv_key_path, enc_key_path)

    # Чтение plaintext
    try:
        plaintext = load_bin_data(input_path)
        print(f"[INFO] Исходный файл прочитан. Размер: {len(plaintext)} байт.")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Исходный файл не найден: {e}")

    # 2.2 Шифрование 3DES-CBC
    block_size = 8  # DES/3DES блок = 8 байт
    iv = os.urandom(block_size)

    try:
        padder = padding.ANSIX923(block_size * 8).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        cipher_algo = get_algo(sym_key)
        cipher = Cipher(cipher_algo, modes.CBC(iv))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()

        final_output = iv + cipher_text
        save_bin_data(final_output, output_path)
    except ValueError as e:
        raise ValueError(f"Ошибка шифрования: {e}")
    except Exception as e:
        raise RuntimeError(f"Критическая ошибка шифрования: {e}")

    print("[STEP 2] Шифрование завершено успешно.\n")


def decrypt_data(
    input_path: str,
    priv_key_path: str,
    enc_key_path: str,
    output_path: str
) -> None:
    """
    Дешифрует файл гибридной системой (RSA + 3DES-CBC).

    1. Восстанавливает симметричный ключ через RSA.
    2. Извлекает IV (первые 8 байт) из зашифрованного файла.
    3. Дешифрует в режиме CBC.
    4. Удаляет паддинг ANSI X.923.

    Args:
        input_path: Путь к зашифрованному файлу.
        priv_key_path: Путь к закрытому ключу RSA.
        enc_key_path: Путь к зашифрованному симметричному ключу.
        output_path: Путь для расшифрованного результата.

    Raises:
        FileNotFoundError: Если файлы отсутствуют.
        ValueError: Если файл слишком мал или неверный ключ/паддинг.
        OSError: При ошибках записи.
    """
    print("[STEP 3] Начало дешифрования данных...")

    # 3.1 Расшифровка симметричного ключа
    sym_key = _decrypt_sym_key(priv_key_path, enc_key_path)

    # Чтение зашифрованного контента
    try:
        encrypted_content = load_bin_data(input_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Зашифрованный файл не найден: {e}")

    block_size = 8
    if len(encrypted_content) < block_size:
        raise ValueError(
            f"Зашифрованный файл слишком мал ({len(encrypted_content)} байт). "
            f"Минимум {block_size} байт для IV."
        )

    iv = encrypted_content[:block_size]
    ciphertext = encrypted_content[block_size:]

    # 3.2 Дешифрование 3DES-CBC
    try:
        cipher_algo = get_algo(sym_key)
        cipher = Cipher(cipher_algo, modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.ANSIX923(block_size * 8).unpadder()
        unpadded_dc_text = unpadder.update(padded_plaintext) + unpadder.finalize()

        save_bin_data(unpadded_dc_text, output_path)
    except ValueError as e:
        raise ValueError(
            f"Ошибка дешифрования (неверный ключ или поврежденные данные): {e}"
        )
    except Exception as e:
        raise RuntimeError(f"Критическая ошибка дешифрования: {e}")

    print("[STEP 3] Дешифрование завершено успешно.\n")
