import alphabet

def encrypt(text, key):
    """
    Шифрует текст шифром Цезаря.

    """
    text = text.upper()
    result = []
    for ch in text:
        if ch in alphabet.alphabet:
            idx = alphabet.alphabet.index(ch)
            new_idx = (idx + key) % len(alphabet.alphabet)
            result.append(alphabet.alphabet[new_idx])
        else:
            result.append(ch)
    return ''.join(result)