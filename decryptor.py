import sys
import json
from pathlib import Path
from typing import Tuple

from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def _fail(message: str, code: int = 1) -> None:
    """Единая точка выхода с ошибкой (DRY)."""
    print(message)
    sys.exit(code)


def _read_file(path: str) -> bytes:
    """Чтение файла с единой обработкой ошибок (DRY)."""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        _fail(f"Файл не найден: {path}")
    except Exception as e:
        _fail(f"Ошибка при чтении файла '{path}': {e}")


def _write_file(path: str, data: bytes) -> None:
    """Запись файла с единой обработкой ошибок (DRY)."""
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        _fail(f"Ошибка при записи файла '{path}': {e}")


def load_private_key(path: str):
    """Загрузка приватного ключа из PEM-файла."""
    print("Загрузка приватного ключа...")
    pem_data = _read_file(path)
    try:
        key = load_pem_private_key(pem_data, password=None)
        print("Ключ загружен.")
        return key
    except Exception as e:
        _fail(f"Ошибка загрузки приватного ключа: {e}")


def decrypt_symmetric_key(encrypted_key: bytes, private_key):
    """Расшифрование симметричного ключа."""
    print("Расшифрование симметричного ключа RSA-ключом.")
    try:
        key = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ расшифрован.")
        return key
    except Exception as e:
        _fail(f"Ошибка при расшифровании симметричного ключа: {e}")


def unpad_data(data: bytes) -> bytes:
    """Удаление ANSI X.923-заполнения."""
    unpadder = sym_padding.ANSIX923(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def aes_decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Расшифрование файла алгоритмом AES-CBC."""
    print(f"Расшифрование файла: {input_path}")
    data = _read_file(input_path)

    if len(data) < 16:
        _fail("Ошибка: зашифрованный файл повреждён или пуст")

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor_obj = cipher.decryptor()

    try:
        padded_plaintext = decryptor_obj.update(ciphertext) + decryptor_obj.finalize()
        plaintext = unpad_data(padded_plaintext)
        _write_file(output_path, plaintext)
        print(f"Файл расшифрован и сохранён: {output_path}")
    except ValueError as e:
        _fail(f"Ошибка при расшифровании — возможно, неверный ключ: {e}")
    except Exception as e:
        _fail(f"Ошибка при расшифровании файла: {e}")


def load_config(config_path: str) -> dict:
    """Загрузка конфигурации из JSON-файла."""
    raw = _read_file(config_path)
    try:
        config = json.loads(raw.decode('utf-8'))
        return config
    except Exception as e:
        _fail(f"Ошибка разбора файла конфигурации: {e}")


def validate_config(config: dict) -> Tuple[str, str, str, str]:
    """Проверка и извлечение обязательных полей конфигурации."""
    match config:
        case {
            "encrypted_file": str(encrypted_file),
            "output_file": str(output_file),
            "encrypted_key_file": str(encrypted_key_file),
            "private_key_file": str(private_key_file)
        } if all(Path(p).exists() for p in (encrypted_key_file, private_key_file)):
            return encrypted_file, output_file, encrypted_key_file, private_key_file
        case _:
            _fail("Ошибка: неверный формат конфигурации или файлы не найдены")


def main() -> None:
    config_path = "config.json"
    config = load_config(config_path)
    encrypted_file, output_file, encrypted_key_file, private_key_file = validate_config(config)

    private_key = load_private_key(private_key_file)

    encrypted_key_data = _read_file(encrypted_key_file)
    aes_key = decrypt_symmetric_key(encrypted_key_data, private_key)

    aes_decrypt_file(encrypted_file, output_file, aes_key)


if __name__ == "__main__":
    main()
