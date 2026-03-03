import constants


def encrypt(text: str, shift: int) -> str:
    """Шифровка текста шифром Цезаря"""

    alphabet_len = len(constants.ALPHABET)
    result = []

    for char in text:
        upper_char = char.upper()

        if upper_char in constants.ALPHABET:
            idx = constants.ALPHABET.index(upper_char)
            new_idx = (idx + shift) % alphabet_len
            result.append(constants.ALPHABET[new_idx])
        else:
            result.append(char)

    return "".join(result)


def decrypt(text: str, shift: int) -> str:
    """Дешифровка"""

    return encrypt(text, -shift)
