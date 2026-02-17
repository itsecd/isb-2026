ALPHABET = "АБВГДЕЖЗИЙКЛМОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
CIPHER =  "ФЖЦЬЭЯЪХЫБЮГЧШРСАИТЛМДКЕУПВЗОН"

def encrypt(text: str) -> str:
    result = ""
    for char in text:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            result += CIPHER[index]
        else:
            result += char
    return result


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read().upper()

    encrypted = encrypt(text)

    with open("encrypted.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    with open("key.txt", "w", encoding="utf-8") as f:
        f.write("OPEN:  " + ALPHABET + "\n")
        f.write("CIPHER:" + CIPHER)