import argparse


def parse_arguments() -> list:
    """
    Парсинг аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", default="cod7.txt", type=str, help="input file")
    parser.add_argument("-o", "--output_text", default="decrypted_text.txt",  type=str, help="output file name")
    parser.add_argument("-k", "--key_file", default="key.txt",  type=str, help="key for the cipher")
    args = parser.parse_args()
    return [args.input_file, args.output_text, args.key_file]


def read_file(file_name: str) -> str:
    """
    Чтение файла
    """
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def save_file(file_name: str, text: str) -> None:
    """
    Сохранение файла
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(text)
    return


def get_letters_frequency(text: str) -> dict[str, int]:
    """
    Получение частоты символов в тексте
    """
    letters = {}
    for i in text:
        if i not in list(letters.keys()):
            letters[i] = 1
        else:
            letters[i] += 1
    for i in letters:
        letters[i] = round(letters[i]/len(text), 4)
    return dict(reversed(sorted(letters.items(), key=lambda item: item[1])))


def decrypt_with_key(cipher: str, key: dict[str, str]) -> str:
    """
    Подстановка символов из ключа в текст
    """
    new_text = cipher
    for i in key:
        new_text = new_text.replace(i, key[i])
    return new_text


def main() -> None:
    try:
        input_file, output_text, key_file = parse_arguments()
        cipher = read_file(input_file)
        print(cipher,'\n')
        letters = get_letters_frequency(cipher)
        print(letters)
        save_file("letters_frequency.txt", str(letters).replace(', ', '\n'))
        key = eval(read_file(key_file).replace("\n", ", "))
        new_text = decrypt_with_key(cipher, key)
        print(new_text)
        save_file("decrypted_text.txt", new_text)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()