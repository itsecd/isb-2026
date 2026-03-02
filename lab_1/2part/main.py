import argparse
import re


def parsing() -> str:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    args = parser.parse_args()
    return args.file_path

def get_text(filename_text: str) -> str:
    "считывание текста из файла"
    with open(filename_text, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def count_frequency(text:str) -> dict:
    """счетчик частот"""
    counter = {}
    for char in text:
        if char == "\n": 
            continue
        if char in counter:
            counter[char] += 1
        else:
            counter[char] = 1
    len_text = len(text)
    frequency = {}
    for char in counter:
            frequency[char] = counter[char]/len_text
    frequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
    return frequency

def write_text(text:str, path:str) -> None:
    "сохранение файлов"
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def dict_to_string(dictionary:dict) -> str:
    """перевод словаря в строку"""
    text = ""
    for char in dictionary:
        val = dictionary[char]
        line = f"{char}: {val} \n"
        text += line
    return text

def unencode_text(encoded_text:str, key:str) -> str:
    """расшифровка текста"""
    mapped_key = {}
    lines = key.split("\n")
    for line in lines:
        line = line.strip()
        match = re.match(r'^"([^"]*)"\s*:\s*"([^"]*)"$', line)
        if match:
            value = match.group(2)
            value_key = match.group(1)
            mapped_key[value_key] = value
    unencoded_text = ""
    for char in encoded_text:
        if char in mapped_key:
            unencoded_text += mapped_key[char]
        else:
            unencoded_text += char
    return unencoded_text

    

def main():
    try:
        filename_text = parsing()
        encoded_text = get_text(filename_text)
        frequency = count_frequency(encoded_text)
        frequency = dict_to_string(frequency)
        write_text(frequency, "frequency.txt")
        key = get_text("key.txt")
        unencoded_text = unencode_text(encoded_text, key)
        write_text(unencoded_text, "unencoded.txt")
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
