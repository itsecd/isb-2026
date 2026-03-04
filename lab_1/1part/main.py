import argparse
from constants import ALPHABET, DECODED_PATH, ENCODED_PATH


def parsing() -> tuple[str, str]:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("key_path", type=str)
    args = parser.parse_args()
    return args.file_path, args.key_path


def get_text(filename: str) -> str:
    "считывание текста из файла"
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def encoded_text(text: str, key: str) -> str:
    "кодирование текста"
    coded_text = ""
    table = []
    key_len = len(key)
    for i in range(len(ALPHABET)):
        table.append(ALPHABET[i:] + ALPHABET[:i])
    for i in range(len(text)):
        if text[i] not in ALPHABET:
            coded_text += text[i]
            continue
        key_idx = i % key_len
        for j in range(len(ALPHABET)):
            if key[key_idx] == ALPHABET[j]:
                idx_width = j
        for n in range(len(ALPHABET)):
            if text[i] == ALPHABET[n]:
                idx_height = n
        coded_text += table[idx_width][idx_height]
    return coded_text


def decoding_text(encoded: str, key: str) -> str:
    "декодирование текста"
    decoded_text = ""
    table = []
    key_len = len(key)
    idx_width = 0
    for i in range(len(ALPHABET)):
        table.append(ALPHABET[i:] + ALPHABET[:i])
    for i in range(len(encoded)):
        if encoded[i] not in ALPHABET:
            decoded_text += encoded[i]
            continue
        key_idx = i % key_len
        for j in range(len(ALPHABET)):
            if key[key_idx] == ALPHABET[j]:
                idx_width = j
        for n in range(len(ALPHABET)):
            if table[idx_width][n] == encoded[i]:
                decoded_text += ALPHABET[n]
    return decoded_text


def write_text(text: str, path: str) -> None:
    "сохранение файлов"
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    try:
        filename_text, filename_key = parsing()
        key = get_text(filename_key)
        text = get_text(filename_text)
        encoded = encoded_text(text, key)
        write_text(encoded, ENCODED_PATH)
        decoded = decoding_text(encoded, key)
        write_text(decoded, DECODED_PATH)
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
