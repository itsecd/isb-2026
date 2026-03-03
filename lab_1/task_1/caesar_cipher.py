"""
Модуль для шифрования и дешифрования текста с использованием шифра Цезаря.
"""

ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def encrypt(plain_text: str, key_shift: int) -> str:
    """
    Шифрует текст с использованием шифра Цезаря.

    Args:
        plain_text: Исходный текст для шифрования.
        key_shift: Величина сдвига (целое число).

    Returns:
        Зашифрованный текст.
    """
    alphabet_length = len(ALPHABET)
    encrypted_chars = []

    for current_char in plain_text:
        upper_char = current_char.upper()

        if upper_char in ALPHABET:
            current_index = ALPHABET.index(upper_char)
            new_index = (current_index + key_shift) % alphabet_length
            encrypted_chars.append(ALPHABET[new_index])
        else:
            encrypted_chars.append(current_char)

    return "".join(encrypted_chars)


def decrypt(encrypted_text: str, key_shift: int) -> str:
    """
    Дешифрует текст, зашифрованный шифром Цезаря.

    Args:
        encrypted_text: Зашифрованный текст для дешифрования.
        key_shift: Величина сдвига, использованная при шифровании.

    Returns:
        Исходный (расшифрованный) текст.
    """
    return encrypt(encrypted_text, -key_shift)