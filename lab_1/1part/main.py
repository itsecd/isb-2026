import argparse


def parsing() -> tuple[str, str]:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("key_path", type=str)
    args = parser.parse_args()
    return args.file_path, args.key_path


def get_text(filename_text: str) -> str:
    "считывание текста из файла"
    with open(filename_text, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def get_key(filename_key: str) -> str:
    "считывание ключа шифрования из файла"
    with open(filename_key, "r", encoding="utf-8") as file:
        key = file.read()
    return key


def encoded_text(text: str, key: str) -> str:
    "кодирование текста"
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    coded_text = ""
    table = []
    key_len = len(key)
    for i in range(len(alphabet)):
        table.append(alphabet[i:] + alphabet[:i])
    for i in range(len(text)):
        if text[i] not in alphabet:
            coded_text += text[i]
            continue
        key_idx = i % key_len
        for j in range(len(alphabet)):
            if key[key_idx] == alphabet[j]:
                idx_width = j
        for n in range(len(alphabet)):
            if text[i] == alphabet[n]:
                idx_height = n
        coded_text += table[idx_width][idx_height]
    return coded_text


def unencoded_text(encoded: str, key: str) -> str:
    "декодирование текста"
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    unencoded_text = ""
    table = []
    key_len = len(key)
    idx_width = 0
    for i in range(len(alphabet)):
        table.append(alphabet[i:] + alphabet[:i])
    for i in range(len(encoded)):
        if encoded[i] not in alphabet:
            unencoded_text += encoded[i]
            continue
        key_idx = i % key_len
        for j in range(len(alphabet)):
            if key[key_idx] == alphabet[j]:
                idx_width = j
        for n in range(len(alphabet)):
            if table[idx_width][n] == encoded[i]:
                unencoded_text += alphabet[n]
    return unencoded_text


def write_text(text:str, path:str) -> None:
    "сохранение файлов"
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    try:
        filename_text, filename_key = parsing()
        key = get_key(filename_key)
        text = get_text(filename_text)
        encoded = encoded_text(text, key)
        write_text(encoded, "EncodedText.txt")
        unencoded = unencoded_text(encoded, key)
        write_text(unencoded, "UnencodedText.txt")
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
