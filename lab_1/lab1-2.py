import argparse


def parse_args():
    """
    Функция для парсинга аргументов командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Путь к файлу с исходным текстом")
    parser.add_argument("-o", "--output", type=str, required=True, help="Путь для записи файла с зашифрованным текстом")
    parser.add_argument("-k", "--key", type=str, required=True, help="Путь до файла с ключом")
    parser.add_argument("-f", "--frequency", type=str, required=True, help="Путь для записи файла с частотами")
    args = parser.parse_args()
    return args.input, args.output, args.key, args.frequency


def create_frequency(text:str) -> str:
    len_t = len(text)
    char_frequency = {i: text.count(i)/len_t for i in text}
    char_frequency = {key: value for key, value in sorted(char_frequency.items(), key= lambda item: item[1], reverse=True)}
    return str(char_frequency)


def decrypt_text(input_text: str, key: dict) -> str:
    result_text = ""
    for i in input_text:
        result_text += key.get(i,i)
    return result_text


def read_key(filepath: str) -> dict:
    key = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for pair in file.readlines():
            key.update(zip(pair[0],pair[1]))
    return key


def write_dict(filepath: str, input_dict: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        for key in input_dict:
            file.write(key+input_dict.get(key)+'\n')

def write_frequency(filepath: str, input_dict: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(input_dict)


def main():
    input_path, output_path, key_path, frequency_path = parse_args()
    with open(input_path, "r", encoding="utf-8") as input_file:
        encoded_text = input_file.read()
    key = read_key("key.txt")
    print(key)
    char_frequency = create_frequency(encoded_text)
    result_text = decrypt_text(encoded_text, key)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(result_text)
    write_frequency(frequency_path, char_frequency)


if __name__ == "__main__":
    main()
