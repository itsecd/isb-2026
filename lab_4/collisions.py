import hashlib
import os
from typing import Literal
import tqdm
from itertools import product


def hash_bruteforce(algo: Literal["sha256", "md5", "sha512"]="md5", first_bytes: int=-1, n: int=3) -> None:
    """
    Функция грубого перебора хешей в поисках коллизий хеш-функции. Перебирает все последовательности длинной N байт.
    Args:
        algo (str): Алгоритм хеширования (хеш-функция)
        first_bytes (int): Сколько первых байт хешей должно совпасть, чтобы они считались коллизией
        n (int): Длинна перебираемых последовательностей байт.
    """
    h = hashlib.new(algo)
    if first_bytes == -1 or first_bytes > h.digest_size: 
        first_bytes = h.digest_size
    
    hashes = dict()
    for it in tqdm.tqdm(product(list(range(0, 256)), repeat=n), ncols=100, desc=f'Поиск коллизий {algo}'):
        byte_s = bytes(it)
        byte_hash = hashlib.new(algo, byte_s).hexdigest()[:first_bytes*2]

        if byte_hash in hashes.keys():
            print(f"\nНайдена коллизия! HEX: {byte_s.hex()}, {hashes[byte_hash].hex()}")
            print(f"Совпадают {first_bytes}/{h.digest_size} байт")
            print(f"{algo} (1): {hashlib.new(algo, byte_s).hexdigest()}")
            print(f"{algo} (2): {hashlib.new(algo, hashes[byte_hash]).hexdigest()}")
            return
        hashes[byte_hash] = byte_s
    print("\nКоллизии не найдены :(")


def hash_bruteforce_random(algo: Literal["sha256", "md5", "sha512"]="md5", first_bytes: int=-1, max_attempts: int=1_000_000) -> None:
    """
    Функция грубого перебора хешей в поисках коллизий хеш-функции. Перебирает случайные последовательности байт длинной digest_size байт
    Args:
        algo (str): Алгоритм хеширования (хеш-функция)
        first_bytes (int): Сколько первых байт хешей должно совпасть, чтобы они считались коллизией
        max_attempts (int): Максимальное кол-во попыток подбора.
    """
    h = hashlib.new(algo)
    if first_bytes == -1 or first_bytes > h.digest_size: 
        first_bytes = h.digest_size
    
    hashes = dict()
    for it in tqdm.trange(max_attempts, ncols=100, desc=f'Поиск коллизий {algo}'):
        random_bytes = os.urandom(h.digest_size)
        hash = hashlib.new(algo, random_bytes).hexdigest()[:first_bytes*2]
        if hash in hashes:
            if hashes[hash] != random_bytes:
                print(f"\nНайдена коллизия! HEX: {random_bytes.hex()}, {hashes[hash].hex()}")
                print(f"Совпадают {first_bytes}/{h.digest_size} байт")
                print(f"{algo} (1): {hashlib.new(algo, random_bytes).hexdigest()}")
                print(f"{algo} (2): {hashlib.new(algo, hashes[hash]).hexdigest()}")
                return
        hashes[hash] = random_bytes
    print("\nКоллизии не найдены :(")


if __name__ == "__main__":
    hash_bruteforce_random(algo="md5", first_bytes=5, max_attempts=1_000_000)