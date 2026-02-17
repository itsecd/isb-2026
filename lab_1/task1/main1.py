import sys


def read(file: str) -> str:

    res = ""
    try:
        with open(file, encoding="utf-8") as f:
            res = f.read()
            return res
    except Exception as e:
        print(e)
        exit(-1)


def encode(text: str, key: str) -> str:
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


def main() -> None:

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



if __name__ == "__main__":
    main()
