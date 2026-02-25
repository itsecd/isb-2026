import sys


def read(file: str) -> str:
    """
    Docstring for read
    Parametrs file: str - path to file with text
    Return readed text: str
    """
    res = ""
    try:
        with open(file, encoding="utf-8") as f:
            res = f.read()
            return res
    except Exception as e:
        print(e)
        exit(-1)


def encode(text: str, key: str) -> str:
    """
    Docstring for encode
    Parametrs text: str, key: str - text for encode with secret key
    Return encoded text: str
    """
    table = []
    rows = len(text) // 10 + 1
    for i in range(rows):
        table.append([""]*10)

    for i in range(rows):
        for j in range(10):
            if i * 10 + j >= len(text):
                break
            table[i][j] = text[i * 10 + j]
    text = ""
    for i in key:
        for j in range(rows):
            text += table[j][int(i)]

    return text


def decode(text: str, key: str) -> str:
    """
    Docstring for decode
    Parametrs text: str, key: str - text for decode with secret key
    Return decoded text: str
    """
    count_of_full = len(text) % 10

    table = []
    rows = len(text) // 10 + 1
    for i in range(rows):
        table.append([""]*10)

    elem = 0
    for i in key:
        i = int(i)
        for j in range(rows):
            if (count_of_full <= i  and j == rows - 1) or elem >= len(text):
                break
            table[j][i] = text[elem]
            elem += 1
    text = ""
    for i in range(rows):
        for j in range(10):
            text += table[i][j]

    return text


def main() -> None:
    """Main functions"""
    if len(sys.argv) != 4:
        print("Use python main1.py input.txt key.txt output.txt")
        exit(-1)

    text = read(sys.argv[1])
    key = read(sys.argv[2])

    text = encode(text, key)

    try:
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            f.write(text)

    except Exception as e:
        print(e)
        exit(-1)
    print(decode(text, key))


if __name__ == "__main__":
    main()
