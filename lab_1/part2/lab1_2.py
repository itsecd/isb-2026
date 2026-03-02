from russian_freq import RUSSIAN_FREQUENCY, ALPHABET

def read_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename: str, text: str):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def calculate_frequency(text: str) -> dict:
    frequency = {}
    total = 0

    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
        total += 1

    for char in frequency:
        frequency[char] = frequency[char] / total

    return frequency


def build_substitution_key(cipher_freq: dict) -> dict:
    sorted_cipher = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_russian = sorted(RUSSIAN_FREQUENCY.items(), key=lambda x: x[1], reverse=True)

    key = {}

    for i in range(min(len(sorted_cipher), len(sorted_russian))):
        cipher_char = sorted_cipher[i][0]
        plain_char = sorted_russian[i][0]
        key[cipher_char] = plain_char

    return key



def load_key_from_file(filename: str) -> dict:
    key = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if "->" in line:
                    parts = line.strip().split("->")
                    if len(parts) == 2:
                        cipher_char = parts[0].strip()
                        plain_char = parts[1].strip()
                        key[cipher_char] = plain_char
    except FileNotFoundError:
        print(f"файл с ключом не найден")
    return key

def decrypt(text: str, key: dict) -> str:
    result = ""

    for char in text:
        if char in key:
            result += key[char]
        else:
            result += char

    return result


def format_frequency(freq: dict) -> str:
    lines = ["СИМВОЛ - ЧАСТОТА\n"]
    for char, value in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"'{char}' - {value:.6f}\n")
    return "".join(lines)


def format_key(key: dict) -> str:
    lines = ["НАЙДЕННЫЙ КЛЮЧ:\n"]
    for cipher_char, plain_char in key.items():
        lines.append(f"{cipher_char} -> {plain_char}\n")
    return "".join(lines)


def main():
    cipher_text = read_file("cipher.txt")

    cipher_frequency = calculate_frequency(cipher_text)
    write_file("frequency.txt", format_frequency(cipher_frequency))

    print("1 - создать новый ключ")
    print("2 - загрузить существующий ключ")

    choice = input("Выбор: ").strip()

    if choice == "2":
        key = load_key_from_file("key.txt")
        if not key:
            print("Ключа нет. Создаем новый...")
            key = build_substitution_key(cipher_frequency)
    else:
        key = build_substitution_key(cipher_frequency)

    write_file("key.txt", format_key(key))

    decrypted_text = decrypt(cipher_text, key)
    write_file("decoded.txt", decrypted_text)



if __name__ == "__main__":
    main()
