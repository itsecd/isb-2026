"""
Демонстрация поиска совпадений первых символов хеша.

Используется tqdm для визуализации процесса.
"""

import hashlib
from tqdm import tqdm


def collision_preview() -> None:
    """
    Выполняет демонстрацию поиска одинаковых
    первых символов SHA256-хеша.
    """

    hashes = {}

    for number in tqdm(range(100000)):
        text = f"message_{number}"

        digest = hashlib.sha256(text.encode()).hexdigest()[:6]

        if digest in hashes:
            print("\nНайдено совпадение:")
            print(f"{hashes[digest]} -> {digest}")
            print(f"{text} -> {digest}")

            return

        hashes[digest] = text


if __name__ == "__main__":
    collision_preview()
