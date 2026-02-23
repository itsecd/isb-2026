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

def write_file(file_path: str) -> str:
    """
    Writing file if it possible
    """
    try:
        with open(file_path, "w", encoding="utf-8") as wfile:
            return rfile.read()
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
                        help="Path to text that should be crypted")
    parser.add_argument("--write_file",
                        "-wf",
                        type=str,
                        help="Path where encrypted text will be saved")
    parser.add_argument("--keyword_file",
                        "-kwf",
                        type=str,
                        help="Path where keyword is located")
    return parser.parse_args()

def encrypting_text(text: str, keyword: str) -> str:
    encrypted_text = ""
    for i, ch in enumerate(text):
        ch1 = ord(ch)
        ch2 = ord(keyword[i % len(keyword)])
        ch3 = (ch1 + ch2) % 127   # просто складываем коды Unicode
        encrypted_text += chr(ch3)
    return encrypted_text

def main() -> None:
    args = parse_args()
    try:
        text = read_file(args.read_file)
        keyword = args.keyword_file
        print(encrypting_text(text, keyword))
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()