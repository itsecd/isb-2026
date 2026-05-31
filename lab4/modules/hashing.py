import os
import hashlib
import bcrypt
import time
from tqdm import tqdm


def generate_salt(length: int = 16) -> bytes:
    """
    Генерирует криптографически стойкую случайную соль.

    Args:
        length (int): длина соли в байтах. По умолчанию 16.

    Returns:
        bytes: случайная соль заданной длины.
    """
    return os.urandom(length)


def hash_password_sha256(password: str, salt: bytes) -> str:
    """
    Вычисляет хеш пароля с использованием SHA-256 и соли.

    Формула: SHA-256(salt + password)

    Args:
        password (str): пароль в открытом виде.
        salt (bytes): соль в виде байтовой строки.

    Returns:
        str: хеш пароля в шестнадцатеричном представлении.
    """
    salted_password = salt + password.encode('utf-8')
    hash_obj = hashlib.sha256(salted_password)
    return hash_obj.hexdigest()


def hash_password_sha256_no_salt(password: str) -> str:
    """
    Вычисляет хеш пароля с использованием SHA-256 без соли.

    Внимание: этот метод небезопасен для реального хранения паролей.
    Используется только для демонстрации уязвимости.

    Args:
        password (str): пароль в открытом виде.

    Returns:
        str: хеш пароля в шестнадцатеричном представлении.
    """
    hash_obj = hashlib.sha256(password.encode('utf-8'))
    return hash_obj.hexdigest()


def hash_password_bcrypt(password: str, salt: bytes) -> str:
    """
    Вычисляет хеш пароля с использованием bcrypt.

    bcrypt автоматически включает соль в хеш и использует
    адаптивную стоимость (количество раундов). По умолчанию 12 раундов.

    Args:
        password (str): пароль в открытом виде.
        salt (bytes): соль (в bcrypt она генерируется автоматически,
                      параметр оставлен для единообразия интерфейса).

    Returns:
        str: хеш пароля в формате bcrypt (включает соль и стоимость).
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode('utf-8')


def hash_password(password: str, salt: bytes, algorithm: str = "sha256") -> str:
    """
    Универсальная функция хеширования пароля.

    Выбирает алгоритм хеширования в зависимости от параметра algorithm.

    Args:
        password (str): пароль в открытом виде.
        salt (bytes): соль.
        algorithm (str): алгоритм хеширования ("sha256" или "bcrypt").
                        По умолчанию "sha256".

    Returns:
        str: хеш пароля.

    Raises:
        ValueError: если указан неподдерживаемый алгоритм.
    """
    match algorithm:
        case "sha256":
            return hash_password_sha256(password, salt)
        case "bcrypt":
            return hash_password_bcrypt(password, salt)
        case _:
            raise ValueError(f"Неподдерживаемый алгоритм хеширования: {algorithm}")


def verify_password_sha256(password: str, salt: bytes, stored_hash: str) -> bool:
    """
    Проверяет соответствие пароля сохранённому хешу SHA-256.

    Args:
        password (str): проверяемый пароль.
        salt (bytes): соль, использованная при хешировании.
        stored_hash (str): сохранённый хеш для сравнения.

    Returns:
        bool: True если пароль верный, иначе False.
    """
    computed_hash = hash_password_sha256(password, salt)
    return computed_hash == stored_hash


def verify_password_bcrypt(password: str, stored_hash: str) -> bool:
    """
    Проверяет соответствие пароля сохранённому хешу bcrypt.

    bcrypt хранит соль внутри хеша, поэтому отдельная соль не нужна.

    Args:
        password (str): проверяемый пароль.
        stored_hash (str): сохранённый хеш bcrypt.

    Returns:
        bool: True если пароль верный, иначе False.
    """
    password_bytes = password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, stored_hash_bytes)


def verify_password(password: str, salt: bytes, stored_hash: str,
                   algorithm: str = "sha256") -> bool:
    """
    Универсальная функция проверки пароля.

    Args:
        password (str): проверяемый пароль.
        salt (bytes): соль (для bcrypt не используется, можно передать b"").
        stored_hash (str): сохранённый хеш.
        algorithm (str): алгоритм хеширования ("sha256" или "bcrypt").

    Returns:
        bool: True если пароль верный, иначе False.

    Raises:
        ValueError: если указан неподдерживаемый алгоритм.
    """
    match algorithm:
        case "sha256":
            return verify_password_sha256(password, salt, stored_hash)
        case "bcrypt":
            return verify_password_bcrypt(password, stored_hash)
        case _:
            raise ValueError(f"Неподдерживаемый алгоритм хеширования: {algorithm}")


def demonstrate_avalanche_effect() -> None:
    """
    Демонстрирует лавинный эффект хеш-функции SHA-256.

    Показывает как минимальное изменение входных данных (один бит)
    приводит к кардинальному изменению выходного хеша.
    Выводит процент изменившихся бит между двумя хешами.
    """
    message1 = "password123"
    message2 = "password124"

    hash1 = hashlib.sha256(message1.encode('utf-8')).hexdigest()
    hash2 = hashlib.sha256(message2.encode('utf-8')).hexdigest()

    print(f"\nДемонстрация лавинного эффекта SHA-256:")
    print(f"Сообщение 1: {message1}")
    print(f"Хеш 1:      {hash1}")
    print(f"\nСообщение 2: {message2}")
    print(f"Хеш 2:      {hash2}")

    bin1 = bin(int(hash1, 16))[2:].zfill(256)
    bin2 = bin(int(hash2, 16))[2:].zfill(256)

    diff_bits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    diff_percent = (diff_bits / 256) * 100

    print(f"\nИзменено бит: {diff_bits} из 256 ({diff_percent:.1f}%)")
    print("Ожидаемое значение при лавинном эффекте: около 50%")


def find_collision_simple(num_bytes: int = 2, show_progress: bool = True) -> dict:
    """
    Ищет коллизию для первых num_bytes байт хеша SHA-256.

    Внимание: это демонстрация для сильно усечённого хеша.
    Для полного SHA-256 подбор коллизии вычислительно невозможен.

    Args:
        num_bytes (int): количество байт хеша для сравнения.
                        По умолчанию 2 (коллизия находится быстро).
        show_progress (bool): показывать ли прогресс-бар через tqdm.

    Returns:
        dict: словарь с результатами поиска:
            - message1 (str): первое сообщение
            - message2 (str): второе сообщение
            - hash_prefix (str): общий префикс хеша
            - attempts (int): количество попыток
            - time_seconds (float): затраченное время
    """
    seen = {}
    attempts = 0
    prefix_len = num_bytes * 2

    start_time = time.time()

    if show_progress:
        pbar = tqdm(desc="Поиск коллизии")
    else:
        pbar = None

    try:
        i = 0
        while True:
            if pbar is not None and attempts % 1000 == 0:
                pbar.set_postfix({
                    "попыток": attempts,
                    "уникальных": len(seen)
                })
                pbar.update(1000)

            message = f"msg_{i}"
            full_hash = hashlib.sha256(message.encode('utf-8')).hexdigest()
            hash_prefix = full_hash[:prefix_len]
            attempts += 1

            if hash_prefix in seen:
                elapsed = time.time() - start_time
                if pbar is not None:
                    pbar.set_postfix({"найдено!": attempts})
                    pbar.close()
                return {
                    "message1": seen[hash_prefix],
                    "message2": message,
                    "hash_prefix": hash_prefix,
                    "attempts": attempts,
                    "time_seconds": elapsed
                }

            seen[hash_prefix] = message
            i += 1

            if attempts >= 10000000:
                if pbar is not None:
                    pbar.close()
                break

    except KeyboardInterrupt:
        if pbar is not None:
            pbar.close()
        print("\nПоиск прерван пользователем.")

    elapsed = time.time() - start_time
    return {
        "message1": None,
        "message2": None,
        "hash_prefix": None,
        "attempts": attempts,
        "time_seconds": elapsed
    }