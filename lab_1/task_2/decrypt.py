# -*- coding: utf-8 -*-
"""Frequency analysis decryption tools."""

import os
import collections
import settings


def load_key() -> dict:
    """Load decryption key from file if it exists."""
    decryption_key: dict = {}
    if os.path.exists(settings.KEY_FILE):
        with open(settings.KEY_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "|" in line:
                    parts: list = line.split("|")
                    cipher_char: str = parts[0].strip()
                    plain_char: str = parts[1].strip()
                    if cipher_char and plain_char:
                        decryption_key[cipher_char] = plain_char[0]
    return decryption_key


def save_key(decryption_key: dict) -> None:
    """Save decryption key to file."""
    with open(settings.KEY_FILE, "w", encoding="utf-8") as file:
        for char in sorted(decryption_key.keys()):
            file.write(f"{char} | {decryption_key[char]}\n")


def main() -> None:
    """Main execution function for frequency analysis decryption."""
    if not os.path.exists(settings.INPUT_FILE):
        print(f"Error: {settings.INPUT_FILE} not found.")
        return

    with open(settings.INPUT_FILE, "r", encoding="utf-8") as file:
        ciphertext: str = file.read()

    clean_text: str = ciphertext.replace("\n", "").replace("\r", "")
    char_counts: collections.Counter = collections.Counter(clean_text)
    total_chars: int = len(clean_text)

    sorted_cipher_chars: list = sorted(
        char_counts.items(), key=lambda x: x[1], reverse=True
    )

    with open(settings.FREQ_FILE, "w", encoding="utf-8") as file:
        for char, count in sorted_cipher_chars:
            file.write(f"'{char}' -> {count / total_chars:.6f}\n")

    current_key: dict = load_key()

    if not current_key:
        print("Key file not found. Generating initial key based on frequency.")
        sorted_ref_chars: list = sorted(
            settings.RUS_FREQ_REF.items(), key=lambda x: x[1], reverse=True
        )

        for i in range(min(len(sorted_cipher_chars), len(sorted_ref_chars))):
            cipher_char: tuple = sorted_cipher_chars[i][0]
            plain_char: tuple = sorted_ref_chars[i][0]
            current_key[cipher_char] = plain_char

        save_key(current_key)
    else:
        print("Key loaded from file.")

    decrypted_text = "".join(current_key.get(c, c) for c in ciphertext)

    with open(settings.DECRYPTED_FILE, "w", encoding="utf-8") as file:
        file.write(decrypted_text)

    print("Decryption completed.")
    print(f"Results saved to: {settings.DECRYPTED_FILE}")
    print("-" * 30)
    print("Output:")
    print(decrypted_text)
    print("-" * 30)


if __name__ == "__main__":
    main()
