alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "


russian_frequency_order = [
    " ", "О", "И", "Е", "А", "Н", "Т", "С", "Р",
    "В", "М", "Л", "Д", "Я", "К", "П", "З", "Ы",
    "Ь", "У", "Ч", "Ж", "Г", "Х", "Ф", "Й",
    "Ю", "Б", "Ц", "Ш", "Щ", "Э", "Ъ"
]


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def count_frequency(text):
    freq = {}

    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1

    return freq


def sort_symbols(freq):
    symbols = list(freq.keys())

    for i in range(len(symbols)):
        for j in range(i + 1, len(symbols)):
            if freq[symbols[i]] < freq[symbols[j]]:
                symbols[i], symbols[j] = symbols[j], symbols[i]

    return symbols


def save_frequency(freq, filename):
    total = 0
    for value in freq.values():
        total += value

    symbols = sort_symbols(freq)

    with open(filename, "w", encoding="utf-8") as file:
        for char in symbols:
            relative = freq[char] / total
            file.write(char + " : " + str(relative) + "\n")


def decoding(text, key):
    result = ""

    for char in text:
        if char in key:
            result += key[char]
        else:
            result += char

    return result


def save_key(key, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for symbol in key:
            file.write(symbol + " -> " + key[symbol] + "\n")


def build_key(sorted_symbols):
    key = {}

    for i in range(len(sorted_symbols)):
        if i < len(russian_frequency_order):
            key[sorted_symbols[i]] = russian_frequency_order[i]

    return key


def load_key(filename):
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
    text = read_file("cod5.txt")

    text = text.replace("G", " ")

    freq = count_frequency(text)

    save_frequency(freq, "TableFrequency_TextEncry.txt")

    key = load_key("Key_Text2.txt")

    if key is None:
        sorted_symbols = sort_symbols(freq)
        key = build_key(sorted_symbols)
        save_key(key, "Key_Text2.txt")
        print("Новый ключ создан.")
    else:
        print("Ключ загружен из файла.")

    decoded = decoding(text, key)

    write_file("ResultDecod_Text2.txt", decoded)

    print("Дешифрование выполнено.")


if __name__ == "__main__":
    main()