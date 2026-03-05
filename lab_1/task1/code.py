`import argparse

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


def build_substitution_table(key: str, alphabet: str, is_reversed:bool = False) -> dict:
    """
    Build substitution table between equal alphabets
    """
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

def load_key(key: str):
    key= read_file("key.txt").replace("'", "")
    for line in key:
        r, c = key.split()
        table[r] = c
    print(table)
    return table



def main() -> None:
    args = parse_args()
    try:
        text = read_file(args.input)
        key = read_file(args.key)
        alphabet = read_file("en_alphabet.txt")

        encryption_table = build_substitution_table(key, alphabet)
        decryption_table = build_substitution_table(key, alphabet, True)

        encrypted_text = encrypting_text(text, load_key(key))
        # decrypted_text = encrypting_text(encrypted_text, decryption_table) #optionally
        write_file(args.output, encrypted_text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()