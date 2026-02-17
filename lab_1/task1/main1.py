import sys


def read(file: str) -> str:

    res = ""
    try:
        with open(file) as f:
            res = f.read()
            return res
    except Exception as e:
        print(e)
        exit(-1)


def main() -> None:

    if len(sys.argv) != 4:
        print("Use python main1.py input.txt key.txt output.txt")
        exit(-1)

    text = read(sys.argv[1])
    key = read(sys.argv[2])

    text = encode(text, key)

    try:
        with open(sys.argv[3], "w") as f:
            f.write(text)

    except Exception as e:
        print(e)
        exit(-1)



if __name__ == "__main__":
    main()
