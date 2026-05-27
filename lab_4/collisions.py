import hashlib
import os
import tqdm
from itertools import product


def md5_bruteforce(first_bytes=16):
    hashes = dict()
    for it in tqdm.tqdm(product(list(range(0, 256)), repeat=3), ncols=100, desc='Поиск коллизий'):
        byte_s = bytes(it)
        byte_hash = hashlib.md5(byte_s).hexdigest()[:first_bytes*2]

        if byte_hash in hashes.keys():
            print(f"\nНайдена коллизия! HEX: {byte_s.hex()}, {hashes[byte_hash].hex()}")
            print(f"Совпадают {first_bytes}/16 байт")
            print(f"MD5 (1): {hashlib.md5(byte_s).hexdigest()}")
            print(f"MD5 (2): {hashlib.md5(hashes[byte_hash]).hexdigest()}")
            return
        hashes[byte_hash] = byte_s
    print("\nКоллизии не найдены :(")


def md5_bruteforce_random(first_bytes=16, max_attempts=1_000_000):
    hashes = dict()
    for it in tqdm.trange(max_attempts, ncols=100, desc='Поиск коллизий'):
        random_bytes = os.urandom(16)
        hash = hashlib.md5(random_bytes).hexdigest()[:first_bytes*2]
        if hash in hashes:
            if hashes[hash] != random_bytes:
                print(f"\nНайдена коллизия! HEX: {random_bytes.hex()}, {hashes[hash].hex()}")
                print(f"Совпадают {first_bytes}/16 байт")
                print(f"MD5 (1): {hashlib.md5(random_bytes).hexdigest()}")
                print(f"MD5 (2): {hashlib.md5(hashes[hash]).hexdigest()}")
                return
        hashes[hash] = random_bytes
    print("\nКоллизии не найдены :(")


def sha256_bruteforce(first_bytes=32):
    hashes = dict()
    for it in tqdm.tqdm(product(list(range(0, 256)), repeat=3), ncols=100, desc='Поиск коллизий'):
        byte_s = bytes(it)
        byte_hash = hashlib.sha256(byte_s).hexdigest()[:first_bytes*2]

        if byte_hash in hashes.keys():
            print(f"\nНайдена коллизия! HEX: {byte_s.hex()}, {hashes[byte_hash].hex()}")
            print(f"Совпадают {first_bytes}/32 байт")
            print(f"MD5 (1): {hashlib.sha256(byte_s).hexdigest()}")
            print(f"MD5 (2): {hashlib.sha256(hashes[byte_hash]).hexdigest()}")
            return
        hashes[byte_hash] = byte_s
    print("\nКоллизии не найдены :(")


def sha256_bruteforce_random(first_bytes=32, max_attempts=1_000_000):
    hashes = dict()
    for it in tqdm.trange(max_attempts, ncols=100, desc='Поиск коллизий'):
        random_bytes = os.urandom(32)
        hash = hashlib.sha256(random_bytes).hexdigest()[:first_bytes*2]
        if hash in hashes:
            if hashes[hash] != random_bytes:
                print(f"\nНайдена коллизия! HEX: {random_bytes.hex()}, {hashes[hash].hex()}")
                print(f"Совпадают {first_bytes}/32 байт")
                print(f"MD5 (1): {hashlib.sha256(random_bytes).hexdigest()}")
                print(f"MD5 (2): {hashlib.sha256(hashes[hash]).hexdigest()}")
                return
        hashes[hash] = random_bytes
    print("\nКоллизии не найдены :(")


if __name__ == "__main__":
    md5_bruteforce_random(first_bytes=5, max_attempts=1_000_000_0)