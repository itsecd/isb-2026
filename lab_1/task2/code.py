import argparse

def read_file(file_path: str) -> str:
    """
    Reading file if it possible
    """
    try:
        with open(file_path, "r", encoding="utf-8") as rfile:
            return rfile.read()
    except FileNotFoundError as e:
        raise

def write_file(file_path: str, text: str) -> str:
    """
    Writing file if it possible
    """
    try:
        with open(file_path, "w", encoding="utf-8") as wfile:
            return wfile.write(text)
    except FileNotFoundError as e:
        raise

def parse_args() -> argparse.Namespace:
    """
    Parse parameters from console
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--read_file",
                        "-rf",
                        type=str,
                        required=True,
                        help="Path to text that should be crypted")
    parser.add_argument("--write_file",
                        "-wf",
                        type=str,
                        required=False,
                        help="Path where encrypted text will be saved")
    parser.add_argument("--key_file",
                        "-kf",
                        type=str,
                        required=False,
                        help="Path where key is located")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    encrypted_text = read_file(args.read_file).replace("\n", "")
    alphabet = "".join(set(encrypted_text)).strip()
    write_file("alphabet.txt", alphabet)

    table = {}
    for ch in alphabet:
        table[ch] = 0
    for ch in encrypted_text:
        table[ch]+=1

    sorted_table = dict(sorted(table.items(), key=lambda item: item[1]))
    print(sorted_table)

if __name__ == "__main__":
    main()