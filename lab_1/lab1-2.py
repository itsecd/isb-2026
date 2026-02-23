import argparse


def parse_args():
    """
    Функция для парсинга аргументов командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Путь к файлу с исходным текстом")
    parser.add_argument("-o", "--output", type=str, required=True, help="Путь для записи файла с зашифрованным текстом")
    parser.add_argument("-k", "--key", type=str, required=True, help="Путь до файла с ключом")
    args = parser.parse_args()
    return args.input, args.output, args.key


def create_frequency(input_str: str) -> dict:
    alphabet=set(input_str)
    frequency = dict.fromkeys(alphabet, 0)
    for j in input_str:
        frequency[j] += (1/len(input_str))


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


def main():
    input_path, output_path, key_path = parse_args()
    with open(input_path, "r", encoding="utf-8") as input_file:
        encoded_text = input_file.read()
    key = read_key("key2.txt")
    result_text = decrypt_text(encoded_text, key)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(result_text)


if __name__ == "__main__":
    main()

