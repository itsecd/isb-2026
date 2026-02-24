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
    parser.add_argument("--key_file",
                        "-kf",
                        type=str,
                        help="Path where key is located")
    return parser.parse_args()

def create_substitution_table(key: str, is_reversed:bool = False) -> set:
    """
    Create substitution table between alphabets
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    table = {}
    if is_reversed == True:
        for i in range(len(alphabet)):
            table[alphabet[i]] = key[i]
    else:
        for i in range(len(alphabet)):
            table[key[i]] = alphabet[i]

    return table

def encrypting_text(text: str, table: set) -> str:
    """
    Encrypting or decrypting text with substitution table
    """
    result = ""
    
    for ch in text:
        if ch in table:
            result += table[ch]
        else:
            result += ch
    return result


def main() -> None:
    args = parse_args()
    try:
        text = read_file(args.read_file)
        key = read_file(args.key_file)

        encryption_table = create_substitution_table(key)
        decryption_table = create_substitution_table(key, True)
        encrypted_text = encrypting_text(text, encryption_table)
        # decrypted_text = encrypting_text(encrypted_text, decryption_table) #optionally
        write_file(args.write_file, encrypted_text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()