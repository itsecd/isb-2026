import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shift", default=13, type=int)
    parser.add_argument("-i", "--input", default="input.txt", type=str)
    parser.add_argument("-o", "--output", default="output.txt", type=str)
    return parser.parse_args()

def read_file(filename: str) -> str:
    '''Returns the content of a file as a string'''
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def write_file(filename: str, content: str) -> None:
    '''Writes content in a file'''
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def caesar_cipher(text: str, shift: int, reverse: bool = False) -> str:
    '''Encodes text using Caesar cipher and return encoded text as a string. If reverse=True decodes.'''
    if reverse:
        shift *= -1
    lower_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    upper_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    result = []
    for char in text:
        if char in lower_alphabet:
            idx = lower_alphabet.index(char)
            new_idx = (idx + shift) % 33
            result.append(lower_alphabet[new_idx])
        elif char in upper_alphabet:
            idx = upper_alphabet.index(char)
            new_idx = (idx + shift) % 33
            result.append(upper_alphabet[new_idx])
        else:
            result.append(char)
    return ''.join(result)

def main():
        args = parse_args()
        to_cipher = read_file(args.input)
        ciphered = caesar_cipher(to_cipher, args.shift)
        write_file(args.output, ciphered)

if __name__ == "__main__":
    main()