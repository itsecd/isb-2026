import argparse
from collections import Counter

def read_file(path: str):
    """
    Reading file if it possible
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise

def write_file(path: str, text: str):
    """
    Writing file if it possible
    """
    try:
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
    except FileNotFoundError as e:
        raise

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-k", "--key", required=True)
    return parser.parse_args()

def get_freq_order(text: str) -> str:
    return "".join(ch for ch, x in Counter(text).most_common())

def build_table(cipher_chars: str) -> dict:
    ru_freq_order = " ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ"
    return {cipher_chars[i]: ru_freq_order[i] for i in range(min(len(cipher_chars), len(ru_freq_order)))}

def decrypt(text: str, table: dict) -> str:
    return "".join(table.get(c, c) for c in text)

def show_preview(text: str, table: dict, limit:int = 300) -> None:
    dec = decrypt(text, table)
    print(dec[:limit])

def swap_chars(table: dict, char1: str, char2: str) -> dict:
    key1 = None
    key2 = None

    for k, v in table.items():
        if v == char1:
            key1 = k
        elif v == char2:
            key2 = k

    if key1 is None or key2 is None:
        print("Одна из букв не найдена в таблице")
        return table

    table[key1], table[key2] = table[key2], table[key1]
    return table

def manual_fixes(text: str, table: dict, limit:int = 300) -> dict:
    print("Automatic replacement")
    show_preview(text, table)
    print("\nEnter exchange: code=letter (for example: P=M). Empty string — finish\n")
    while True:
        cmd = input("> ").strip().upper()
        if not cmd:
            break

        c, r = cmd.split("=")
        table = swap_chars(table, c, r)
        show_preview(text, table)
    return table


def save_key(table: dict, path: str):
    if not path:
        return
    with open(path, "w", encoding="utf-8") as f:
        for c, p in sorted(table.items(), key=lambda x: x[1]):
            f.write(f"{repr(c):>4} = {repr(p)}\n")

def main():
    args = parse_args()
    text = read_file(args.input)

    order = get_freq_order(text)
    table = build_table(order)

    table_key = manual_fixes(text, table)
    save_key(table_key, args.key)
    decrypted_text = decrypt(text, table_key)

    write_file(args.output, decrypted_text)

    print("Decrypted text:")
    print(decrypted_text)


if __name__ == "__main__":
    main()