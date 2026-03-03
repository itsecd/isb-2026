
""" Реализация дешифрования данного текста методом частотного анализа. """

from constants import (
    RUSSIAN_FREQUENCY_ORDER,
    COD_FILE,
    FREQ_TABLE_FILE,
    KEY_FILE,
    RESULT_FILE
)


def read_file(filename):

    """ Чтение содержимого файла. """

    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, text):

    """ Запись переданного текста в файл. """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def count_frequency(text):

    """ Вычисление относительной частоты символом в данном тексте. """

    counts = {}
    total = len(text)

    for char in text:
        counts[char] = counts.get(char, 0) + 1

    frequency = {}
    for char, count in counts.items():
        frequency[char] = count / total

    return frequency


def sort_symbols(freq):

    """ Сортировка используемых символов по убыванию их частоты. """

    symbols = list(freq.keys())

    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            if freq[symbols[i]] < freq[symbols[j]]:
                symbols[i], symbols[j] = symbols[j], symbols[i]

    return symbols


def save_frequency(freq, filename):

    """ Сохранение таблицы частот символов в файл. """

    total = 0
    for value in freq.values():
        total += value

    symbols = sort_symbols(freq)

    with open(filename, "w", encoding="utf-8") as file:
        for char in symbols:
            relative = freq[char] / total
            file.write(char + " : " + str(relative) + "\n")


def decoding(text, key):

    """ Расшифровка текста с использованием ключа замены. """

    result = ""

    for char in text:
        if char in key:
            result += key[char]
        else:
            result += char

    return result


def save_key(key, filename):

    """ Сохранение ключа замены в файл. """

    with open(filename, "w", encoding="utf-8") as file:
        for symbol in key:
            file.write(symbol + " -> " + key[symbol] + "\n")


def build_key(sorted_symbols):

    """ Формирование ключа замены на основе частот символов. """

    key = {}

    for i in range(len(sorted_symbols)):
        if i < len(RUSSIAN_FREQUENCY_ORDER):
            key[sorted_symbols[i]] = RUSSIAN_FREQUENCY_ORDER[i]

    return key


def load_key(filename):

    """ Загрузка ключа замены из файла. """

    key = {}

    try:
        file = open(filename, "r", encoding="utf-8")
    except OSError:
        return None

    for line in file:
        parts = line.replace("\n", "").split(" -> ")
        if len(parts) == 2:
            key[parts[0]] = parts[1]

    file.close()
    return key


def main():

    """ Главная функция. """

    text = read_file(COD_FILE)

    text = text.replace("G", " ")

    freq = count_frequency(text)

    save_frequency(freq, FREQ_TABLE_FILE)

    key = load_key(KEY_FILE)

    if key is None:
        sorted_symbols = sort_symbols(freq)
        key = build_key(sorted_symbols)
        save_key(key, KEY_FILE)
        print("Новый ключ создан.")
    else:
        print("Ключ загружен из файла.")

    decoded = decoding(text, key)

    write_file(RESULT_FILE, decoded)

    print("Дешифрование выполнено.")


if __name__ == "__main__":
    main()