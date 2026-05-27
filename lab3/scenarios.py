import rsa_keys
import symmetric
import file_io


def _load_crypto_context(private_key_path: str, encrypted_sym_key_path: str, nonce_path: str):
    """
    Загрузка криптографического контекста: закрытого ключа, симметричного ключа и nonce.

    Args:
        private_key_path: Путь к закрытому RSA-ключу.
        encrypted_sym_key_path: Путь к зашифрованному симметричному ключу.
        nonce_path: Путь к файлу с nonce.

    Returns:
        tuple[bytes, bytes]: Расшифрованный симметричный ключ и nonce.

    Raises:
        FileNotFoundError: Один из файлов не найден.
        ValueError: Некорректные данные ключа или nonce.
        RuntimeError: Ошибка при загрузке или дешифровании.
    """
    try:
        private_key = rsa_keys.load_private_key(private_key_path)
        encrypted_sym_key = symmetric.load_encrypted_sym_key(encrypted_sym_key_path)
        sym_key = rsa_keys.rsa_decrypt(private_key, encrypted_sym_key)
        nonce = symmetric.load_nonce(nonce_path)
        return sym_key, nonce
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден при загрузке контекста: {e}")
    except ValueError as e:
        raise ValueError(f"Некорректные данные при загрузке контекста: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке криптографического контекста: {e}")


def generate_keys(nonce_path: str, encrypted_sym_key_path: str, public_key_path: str, private_key_path: str) -> None:
    """
    1: Генерация ключей гибридной системы.

    Args:
        nonce_path: Путь для сохранения nonce.
        encrypted_sym_key_path: Путь для сохранения зашифрованного симметричного ключа.
        public_key_path: Путь для сохранения открытого RSA-ключа.
        private_key_path: Путь для сохранения закрытого RSA-ключа.

    Raises:
        RuntimeError: Ошибка при генерации ключей.
    """
    print("\nГенерация ключей (ChaCha20 + RSA)\n" + "─" * 60)

    try:
        sym_key = symmetric.generate_sym_key()
        nonce = symmetric.generate_nonce()

        private_key, public_key = rsa_keys.generate_rsa_keys(key_size=2048)
        rsa_keys.save_rsa_keys(private_key, public_key, private_key_path, public_key_path)

        encrypted_sym_key = rsa_keys.rsa_encrypt(public_key, sym_key)
        symmetric.save_encrypted_sym_key(encrypted_sym_key, encrypted_sym_key_path)
        symmetric.save_nonce(nonce, nonce_path)

        print("─" * 60)
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации ключей: {e}")


def encrypt_data(input_file: str, private_key_path: str, encrypted_sym_key_path: str, nonce_path: str, output_file: str) -> None:
    """
    2: Шифрование данных гибридной системой.

    Args:
        input_file: Путь к исходному файлу для шифрования.
        private_key_path: Путь к закрытому RSA-ключу.
        encrypted_sym_key_path: Путь к зашифрованному симметричному ключу.
        nonce_path: Путь к файлу с nonce.
        output_file: Путь для сохранения зашифрованного файла.

    Raises:
        FileNotFoundError: Входной файл или ключи не найдены.
        RuntimeError: Ошибка при шифровании. 
    """
    print("\nШифрование данных (ChaCha20 + RSA)\n" + "─" * 60)
    try:
        sym_key, nonce = _load_crypto_context(private_key_path, encrypted_sym_key_path, nonce_path)
        plaintext = file_io.read_file(input_file)
        ciphertext = symmetric.chacha20_crypt(plaintext, sym_key, nonce)
        file_io.write_file(output_file, ciphertext)

        print("─" * 60)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Ошибка шифрования: файл не найден - {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании: {e}")


def decrypt_data(input_file: str, private_key_path: str, encrypted_sym_key_path: str, nonce_path: str, output_file: str) -> None:
    """
    3: Дешифрование данных гибридной системой.

    Args:
        input_file: Путь к зашифрованному файлу.
        private_key_path: Путь к закрытому RSA-ключу.
        encrypted_sym_key_path: Путь к зашифрованному симметричному ключу.
        nonce_path: Путь к файлу с nonce.
        output_file: Путь для сохранения расшифрованного файла.

    Raises:
        FileNotFoundError: Входной файл или ключи не найдены.
        RuntimeError: Ошибка при дешифровании.
    """
    print("\nДешифрование данных (ChaCha20 + RSA)\n" + "─" * 60)
    try:
        sym_key, nonce = _load_crypto_context(private_key_path, encrypted_sym_key_path, nonce_path)
        ciphertext = file_io.read_file(input_file)
        plaintext = symmetric.chacha20_crypt(ciphertext, sym_key, nonce)
        file_io.write_file(output_file, plaintext)

        print("─" * 60)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Ошибка дешифрования: файл не найден - {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при дешифровании: {e}")
