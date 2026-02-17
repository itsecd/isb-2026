def load_key(filepath):
    key = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if " -> " in line:
                parts = line.split(" -> ")
                if len(parts) == 2:
                    cipher_char = parts[0]
                    plain_char = parts[1].strip('\n\r')

                    if not plain_char:
                        plain_char = " "

                    key[cipher_char] = plain_char
    return key


def decrypt(text, key):
    return "".join(key.get(c, c) for c in text)


def main():
    key_file = "found_key.txt"
    input_file = "cod15.txt"
    output_file = "decrypted.txt"

    try:
        key = load_key(key_file)

        with open(input_file, "r", encoding="utf-8") as f:
            cipher_text = f.read()

        result = decrypt(cipher_text, key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)


    except FileNotFoundError as e:
        print(f"Не найден файл {e.filename}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()