import random


def main() -> None:
    """
    Docstring for main
    """
    res = ""
    for i in range(128):
        res += str(random.randint(0, 1))

    with open("py.txt", "w") as f:
        f.write(res)


if __name__ == "__main__":
    main()
