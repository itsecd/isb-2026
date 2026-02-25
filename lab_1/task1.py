from text_key import KEY
from constants import ALPHABET_SET, ALPHABET_LIST, TASK1_INPUT, TASK1_OUTPUT

def encode(text: str, key: str) -> str:
    """Шифр Виженера"""
    if not set(key).issubset(ALPHABET_SET):
        raise Exception("Ошибка ключа")
    res = ""

    n = 0
    for c in text:
        if c in ALPHABET_SET:
            shift = ALPHABET_LIST.index(key[n % len(key)]) 
            res += ALPHABET_LIST[(ALPHABET_LIST.index(c) + shift) % len(ALPHABET_LIST)]
            n += 1
        else:
            res += c
    return res

def decode(text: str, key: str) -> str:
    """Шифр Виженера"""
    if not set(key).issubset(ALPHABET_SET):
        raise Exception("Ошибка ключа")
    res = ""

    n = 0
    for c in text:
        if c in ALPHABET_SET:
            shift = ALPHABET_LIST.index(key[n % len(key)])
            res += ALPHABET_LIST[(ALPHABET_LIST.index(c) - shift) % len(ALPHABET_LIST)]
            n += 1
        else:
            res += c
    return res



def main() -> None:
    with open(TASK1_INPUT, encoding="utf-8", mode="r") as f:
        data = f.read()
    data = data.replace("\n", " ").upper()

    print(enc := encode(data, KEY))

    with open(TASK1_OUTPUT, encoding="utf-8", mode="w") as f:
        f.write(enc)
    print()
    print(decode(enc, KEY))


if __name__ == "__main__":
    main()