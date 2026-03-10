import random


def build_sequence(size: int = 128) -> str:
    bits = [str(random.getrandbits(1)) for _ in range(size)]
    return "".join(bits)


def main() -> None:
    sequence = build_sequence()

    with open("seq_python.txt", "w", encoding="utf-8") as file:
        file.write(sequence)


if __name__ == "__main__":
    main()
