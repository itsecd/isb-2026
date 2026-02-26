from const import *

def frequency(text):
    """Подсчёт частоты символов"""
    frequency = {}
    len_txt = len(text)

    if len_txt == 0:
        return {}

    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    for char in frequency:
        frequency[char] = frequency[char] / len_txt

    return frequency


def read_mapping(filename):
    """Создание словаря замен"""
    mapping = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.split('=', 1)
            if key == '\\n':
                key = '\n'
            mapping[key] = value.strip('\n')

    return mapping


def decrypt_text(text, mapping):
    """Расшифровка текста"""
    result = []
    for char in text:
        if char in mapping:
            result.append(mapping[char])
        else:
            result.append(char)
    return ''.join(result)


def main():
    with open(COD24, 'r', encoding='utf-8') as f:
        text = f.read()

    freq = frequency(text)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    with open(FREQUENCY, 'w', encoding='utf-8') as f:
        for key, value in sorted_freq:
            f.write(f"'{key}' = {value:.4f}\n")

    mapping = read_mapping(KEY)

    decrypted = decrypt_text(text, mapping)

    with open(TEXT_DECRYPTION, 'w', encoding='utf-8') as f:
        f.write(decrypted)


if __name__ == "__main__":
    main()