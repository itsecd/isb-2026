"""Модуль реализации шифра Цезаря."""

from alphabet import ALPHABET


def encrypt(text: str, shift: int) -> str:
    """
    Зашифровать текст методом Цезаря.

    Каждая буква алфавита сдвигается на заданное
    количество позиций вправо.

    Args:
        text: Исходный текст.
        shift: Величина сдвига.

    Returns:
        Зашифрованный текст.
    """
    result = []

    for char in text:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            new_index = (index + shift) % len(ALPHABET)
            result.append(ALPHABET[new_index])
        else:
            result.append(char)

    return "".join(result)


def decrypt(text: str, shift: int) -> str:
    """
    Расшифровать текст, зашифрованный методом Цезаря.

    Args:
        text: Зашифрованный текст.
        shift: Величина сдвига.

    Returns:
        Расшифрованный текст.
    """
    return encrypt(text, -shift)
