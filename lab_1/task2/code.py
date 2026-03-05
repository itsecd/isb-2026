import argparse
from collections import Counter


def read_file(path: str) -> str:
    """
    Read file content.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise


def write_file(path: str, text: str) -> None:
    """
    Write text to file.
    """
    try:
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write(text)
    except FileNotFoundError:
        raise


def parse_args() -> argparse.Namespace:
    """
    Parse parameters from console.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-k", "--key", required=True)
    return parser.parse_args()


def get_freq_order(text: str) -> str:
    """
    Return characters ordered by frequency.
    """
    return "".join(ch for ch, _ in Counter(text).most_common())


def write_freq_order(text: str) -> str:
    """
    Return formatted frequency table as string.
    """
    total = len(text)
    counter = Counter(text)
    lines = []

    for ch, count in counter.most_common():
        freq = count / total
        lines.append(f"{ch} = {freq:.6f}")

    return "\n".join(lines)


def build_table(cipher_chars: str, freq_order: str) -> dict:
    """
    Build substitution table.
    """

    return {
        cipher_chars[i]: freq_order[i]
        for i in range(min(len(cipher_chars), len(freq_order)))
    }


def decrypt(text: str, table: dict) -> str:
    """
    Decrypt text using substitution table.
    """
    return "".join(table.get(char, char) for char in text)


def show_preview(text: str, table: dict, limit: int = 500) -> None:
    """
    Print preview of decrypted text.
    """
    decrypted = decrypt(text, table)
    print(decrypted[:limit])


def swap_chars(table: dict, char1: str, char2: str) -> dict:
    """
    Swap two characters in substitution table.
    """
    key1 = None
    key2 = None

    for key, value in table.items():
        if value == char1:
            key1 = key
        elif value == char2:
            key2 = key

    if key1 is None or key2 is None:
        print("One of the letters is not found in the table")
        return table

    table[key1], table[key2] = table[key2], table[key1]
    return table


def manual_fixes(text: str, table: dict) -> dict:
    """
    Allow manual substitution fixes.
    """
    print("Automatic replacement")
    show_preview(text, table)
    print(
        "\nEnter exchange: code=letter "
        "(for example: P=M). Empty string — finish\n"
    )

    while True:
        cmd = input("> ").strip().upper()

        if not cmd:
            break

        cipher_char, real_char = cmd.split("=")
        table = swap_chars(table, cipher_char, real_char)
        show_preview(text, table)

    return table


def save_key(table: dict, path: str) -> None:
    """
    Save substitution key to file.
    """
    if not path:
        return


    with open(path, "w", encoding="utf-8") as file:
        lines = [
            f"{cipher_char}->{plain_char}"
            for cipher_char, plain_char in sorted(
                table.items(), key=lambda item: item[1]
            )
        ]
        file.write("\n".join(lines))



def load_key(key: str):
    table = dict()
    key= read_file("key.txt").split("\n")
    for line in key:
        r, c = line.split("->")
        table[r] = c
    return table


def main() -> None:
    args = parse_args()
    text = read_file(args.input).replace("\n", "")

    write_file("freq_text_alph.txt", write_freq_order(text))

    order = get_freq_order(text)
    table = build_table(order, read_file("freq_ru_alph.txt"))

    table_key = manual_fixes(text, table)
    save_key(table_key, args.key)

    decrypted_text = decrypt(text, table_key)
    # decrypted_text = decrypt(text, load_key(args.key))
    write_file(args.output, decrypted_text)

    print("Decrypted text:")
    print(decrypted_text)


if __name__ == "__main__":
    main()