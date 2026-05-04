import os
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives import padding

def generate_key_for_IDEA(key_size: int) -> bytes:
    """Создаёт ключ для алгоритма IDEA."""
    if key_size != 16:
        raise ValueError(
            f"IDEA требует ключ 16 байт (128 бит)."
            f"Получено из настроек: {key_size} байт."
        )
    try:
        key = os.urandom(key_size)
        if all(b == 0 for b in key):
            raise RuntimeError("Сгенерирован нулевой ключ - возможна проблема с RNG")
        return key
    except NotImplementedError as e:
        raise RuntimeError(f"Система не поддерживает криптографически стойкий RNG: {e}") from e
    except OSError as e:
        raise RuntimeError(f"Ошибка при чтении из /dev/urandom: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка при генерации ключа: {e}") from e


def generate_iv(iv_size: int) -> bytes:
    """Генерирует мусорное значение iv для режима CBC."""
    if iv_size != 8:
        raise ValueError(
            f"IDEA в режиме CBC требует IV размером 8 байт (64 бита)."
            f"Получено из настроек: {iv_size} байт."
        )
    try:
        iv = os.urandom(iv_size)
        if all(b == 0 for b in iv):
            raise RuntimeError("Сгенерирован нулевой iv - возможна проблема с RNG")
        return iv
    except NotImplementedError as e:
        raise RuntimeError(f"Система не поддерживает криптографически стойкий RNG: {e}") from e
    except OSError as e:
        raise RuntimeError(f"Ошибка при генерации iv: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка при генерации iv: {e}") from e


def make_padding(data: bytes, block_size_bits: int) -> bytes:
    """Дополняет данные до размера(используя паддинг), кратного размеру блока."""
    if not isinstance(data, bytes):
        raise TypeError(f"Данные должны быть типа bytes, получен {type(data).__name__}")
    if block_size_bits != 64:
        raise ValueError(
            f"IDEA использует блоки только 64 бит."
            f"Получено из настроек: {block_size_bits} бит."
        )
    if block_size_bits % 8 != 0:
        raise ValueError(f"Размер блока в битах должен быть кратен 8, получено {block_size_bits}")
    try:
        padder = padding.ANSIX923(block_size_bits).padder()
        data_with_padding = padder.update(data) + padder.finalize()
        return data_with_padding
    except ValueError as e:
        raise ValueError(f"Ошибка при применении паддинга ANSI X.923: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка при паддинге: {e}") from e


def make_unpadding(data_with_padding: bytes, block_size_bits: int) -> bytes:
    """Выполняет депаддинг в расшифрованных данных."""
    if not isinstance(data_with_padding, bytes):
        raise TypeError(f"Данные должны быть типа bytes, получен {type(data_with_padding).__name__}")
    if len(data_with_padding) == 0:
        raise ValueError("Невозможно удалить паддинг: данные пусты")
    if block_size_bits != 64:
        raise ValueError(
            f"IDEA использует блоки только 64 бит."
            f"Получено из настроек: {block_size_bits} бит."
        )
    block_size_bytes = block_size_bits // 8
    if len(data_with_padding) % block_size_bytes != 0:
        raise ValueError(
            f"Данные не выровнены: {len(data_with_padding)} байт, "
            f"размер блока {block_size_bytes} байт"
        )
    try:
        unpadder = padding.ANSIX923(block_size_bits).unpadder()
        original_data = unpadder.update(data_with_padding) + unpadder.finalize()
        return original_data
    except ValueError as e:
        raise ValueError(f"Ошибка при удалении паддинга (возможно, данные повреждены): {e}") from e
    except Exception as e:
        raise RuntimeError(f"Неожиданная ошибка при удалении паддинга: {e}") from e


def encrypt_data(key: bytes, iv: bytes, plaintext: bytes, block_size_bits: int) -> bytes:
    """Шифрует данные алгоритмом IDEA в режиме CBC."""
    if not isinstance(key, bytes) or len(key) != 16:
        raise ValueError(f"Ключ IDEA должен быть 16 байт, получено {len(key) if isinstance(key, bytes) else 'не bytes'}")
    
    if not isinstance(iv, bytes) or len(iv) != 8:
        raise ValueError(f"iv для IDEA должен быть 8 байт, получено {len(iv) if isinstance(iv, bytes) else 'не bytes'}")
    
    if not isinstance(plaintext, bytes):
        raise TypeError(f"Открытый текст должен быть bytes, получен {type(plaintext).__name__}")
    
    if block_size_bits != 64:
        raise ValueError(
            f"IDEA использует блоки 64 бит. "
            f"Получено: {block_size_bits} бит. "
        )
    try:
        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = make_padding(plaintext, block_size_bits)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return ciphertext
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании IDEA: {e}") from e



def decrypt_data(key: bytes,iv: bytes,ciphertext: bytes,block_size_bits: int,key_size: int = None,iv_size: int = None) -> bytes:
    """Расшифровывает данные алгоритмом IDEA в режиме CBC."""
    if key_size is not None and key_size != 16:
        raise ValueError(
            f"IDEA требует ключ 16 байт. Получено из настроек: {key_size} байт."
        )
    
    if iv_size is not None and iv_size != 8:
        raise ValueError(
            f"IDEA требует iv 8 байт. Получено из настроек: {iv_size} байт."
        )
    
    if block_size_bits != 64:
        raise ValueError(
            f"IDEA использует блоки 64 бит. Получено из настроек: {block_size_bits} бит."
        )
    _validate_key(key)
    _validate_iv(iv)
    if not isinstance(ciphertext, bytes):
        raise TypeError(f"Шифротекст должен быть bytes, получен {type(ciphertext).__name__}")
    
    if len(ciphertext) == 0:
        raise ValueError("Невозможно расшифровать пустые данные")
    
    block_size_bytes = block_size_bits // 8
    if len(ciphertext) % block_size_bytes != 0:
        raise ValueError(
            f"Шифротекст повреждён: длина {len(ciphertext)} байт не кратна "
            f"размеру блока {block_size_bytes} байт"
        )
    try:
        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        original_data = make_unpadding(decrypted_padded, block_size_bits)
        return original_data
    except ValueError as e:
        raise ValueError(f"Ошибка при дешифровании: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка при дешифровании: {e}") from e


def _validate_key(key: bytes) -> None:
    """Внутренняя проверка ключа."""
    if not isinstance(key, bytes):
        raise TypeError(f"Ключ должен быть bytes, получен {type(key).__name__}")
    if len(key) != 16:
        raise ValueError(f"IDEA ключ должен быть 16 байт, получено {len(key)} байт")


def _validate_iv(iv: bytes) -> None:
    """Внутренняя проверка IV."""
    if not isinstance(iv, bytes):
        raise TypeError(f"IV должен быть bytes, получен {type(iv).__name__}")
    
    if len(iv) != 8:
        raise ValueError(f"IV для IDEA должен быть 8 байт, получено {len(iv)} байт")