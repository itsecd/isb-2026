A_set = set("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
A_list = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")


def encode(text: str, key: str) -> str:
    """Шифр Виженера"""
    if not set(key).issubset(A_set):
        return text # Ошибка ключа
    res = ""

    n = 0
    for c in text:
        if c in A_set:
            shift = A_list.index(key[n % len(key)]) 
            res += A_list[(A_list.index(c) + shift) % len(A_list)]
            n += 1
        else:
            res += c
    return res

def decode(text: str, key: str) -> str:
    """Шифр Виженера"""
    if not set(key).issubset(A_set):
        return text # Ошибка ключа
    res = ""

    n = 0
    for c in text:
        if c in A_set:
            shift = A_list.index(key[n % len(key)])
            res += A_list[(A_list.index(c) - shift) % len(A_list)]
            n += 1
        else:
            res += c
    return res



def main() -> None:
    with open("lab_1/text.txt", encoding="utf-8", mode="r") as f:
        data = f.read()
    data = data.replace("\n", " ").upper()

    print(enc := encode(data, "ШИФР"))

    with open("lab_1/text_enc.txt", encoding="utf-8", mode="w") as f:
        f.write(enc)
    #print(decode(code, "ШИФР"))


if __name__ == "__main__":
    main()