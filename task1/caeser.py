import ALPHABET

def encrypt(text: str, key: int) -> str:
    """
    Шифрует текст шифром Цезаря.
    """
    text = text.upper()
    alphabet = ALPHABET.ALPHABET
    key = key % len(alphabet)
    shifted = alphabet[key:] + alphabet[:key]
    translator = str.maketrans(alphabet, shifted)
    return text.translate(translator)


def decrypt(text: str, key: int) -> str:
    """
    Дешифрует текст.
    """
    text = text.upper()
    alphabet = ALPHABET.ALPHABET
    key = key % len(alphabet)
    shifted = alphabet[-key:] + alphabet[:-key] if key != 0 else alphabet
    translator = str.maketrans(alphabet, shifted)
    return text.translate(translator)