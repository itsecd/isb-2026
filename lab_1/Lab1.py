import argparse



def parse_arguments() -> list:
    """
    Парсинг аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", default="randomtext.txt", type=str, help="input  file")
    parser.add_argument("-o", "--output_cipher", default="cipher.txt",  type=str, help="output  file")
    parser.add_argument("-k", "--key_word", default="маркс",  type=str, help="key for the cipher")
    args = parser.parse_args()
    return [args.input_file, args.output_cipher, args.key_word]


def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read().lower()
    return text


def make_alphabet(alphabet_file_name: str) -> dict[str, int]:
    with open(alphabet_file_name, "r", encoding="utf-8") as file:
        text = file.read().lower().split(", ")
    alphabet = {}
    for i in range(len(text)):
        alphabet[text[i]]=i
    return alphabet


def vigenere_encryption(base_text: str, key: str, alphabet: dict[str, int]) -> str:
    cipher = ""
    j = 0
    for i in range(len(base_text)):
        if base_text[i] in list(alphabet.keys()):
            m = (alphabet[base_text[i]] + alphabet[key[j]])%len(alphabet)
            cipher += list(alphabet.keys())[m]
            j = (j+1)%len(key)
        else:
            cipher += base_text[i]
    return cipher


def vigenere_decryption(cipher: str, key: str, alphabet: dict[str, int]) -> str:
    text = ""
    j = 0
    for i in range(len(cipher)):
        if cipher[i] in list(alphabet.keys()):
            m = (alphabet[cipher[i]] - alphabet[key[j]])%len(alphabet)
            text += list(alphabet.keys())[m]
            j = (j+1)%len(key)
        else:
            text += cipher[i]
    return text


def main() -> None:
    try:
        input_file, output_cipher, key = parse_arguments()
        alphabet = make_alphabet("alphabet.txt")
        text = read_file(input_file)
        print(text,'\n')
        cipher = vigenere_encryption(text, key, alphabet)
        print(cipher, '\n')
        new_text = vigenere_decryption(cipher, key, alphabet)
        print(new_text)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()