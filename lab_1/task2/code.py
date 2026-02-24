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

def create_substitution_table(key: str, is_reversed:bool = False) -> set:
    """
    Create substitution table between alphabets
    """
    alphabet = "ЪЭЩШЦБЮЙФХГЧЬЫЗПКЯДЛМВРТСНАЕИО "
    table = {}
    if is_reversed == True:
        for i in range(len(alphabet)):
            table[alphabet[i]] = key[i]
    else:
        for i in range(len(alphabet)):
            table[key[i]] = alphabet[i]

    return table

def create_freq_analysis(text: str) -> str:
    table = {}
    for ch in text:
        if ch not in table:
            table[ch] = 1
        else:
            table[ch] += 1

    total_chars = sum(table.values()) 
    freq_table = {k: v / total_chars for k, v in table.items()}

    sorted_table = dict(sorted(freq_table.items(), key=lambda item: item[1], reverse=True))

    result = '\n'.join(f"{k} = {v:.6f}" for k, v in sorted_table.items())
    return result

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
    encrypted_text = read_file(args.read_file).replace("\n", "")

    table = create_freq_analysis(encrypted_text)
    write_file(args.write_file, table)

if __name__ == "__main__":
    main()