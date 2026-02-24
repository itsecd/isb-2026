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

def create_substitution_table(key: str) -> set:
    """
    Create substitution table between alphabets
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    table = {}
    for i in range(27):
        table[alphabet[i]] = keyword[i]
    return table

def encrypting_text(text: str, table: set) -> str:
    """
    Encrypting text with substitution table
    """

    text = text.lower()
    encrypted_text = ""
    for ch in text:
        for
        encrypted_text += chr(ch3)
    return encrypted_text

# def decrypting_text(encrypted_text: str, table: set) -> str:
#     """
#     Decrypting text with substitution table
#     """
#     decrypted_text = ""
#     for i, ch in enumerate(encrypted_text):
#         ch1 = ord(ch)
#         ch2 = ord(keyword[i % len(keyword)])
#         ch3 = ch1 - ch2
#         decrypted_text += chr(ch3)
#     return decrypted_text

def main() -> None:
    args = parse_args()
    try:
        text = read_file(args.read_file)
        keyword = args.keyword_file
        encrypted_text = encrypting_text(text, args.keyword_file)
        decrypted_text = decrypting_text(encrypted_text, args.keyword_file)
        write_file(args.write_file, encrypted_text)
        write_file(args.write_file, decrypted_text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()