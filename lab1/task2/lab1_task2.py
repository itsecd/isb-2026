import ru_freq


def load_text(filename):
    """
    Загружает текст из файла
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def save_text(filename, text):
    """
    Сохраняет текст в файл
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def analyze_frequency(text):
    """
    Анализирует частоту символов и сохраняет в freq.txt
    """
    text_plain = text.replace('\n', '')
    total = len(text_plain)

    freq = {}
    for char in text_plain:
        freq[char] = freq.get(char, 0) + 1

    items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    with open('freq.txt', 'w', encoding='utf-8') as f:
        for char, count in items:
            freq_value = count / total
            f.write(f"{char} = {freq_value:.5f}\n")

    return items


def build_key(text_freq):
    """
    Создает ключ 
    """
    text_chars = [char for char, _ in text_freq]

    russian_items = sorted(ru_freq.FREQ.items(), key=lambda x: x[1], reverse=True)
    russian_chars = [char for char, _ in russian_items]

    key = {}
    for i in range(min(len(text_chars), len(russian_chars))):
        key[text_chars[i]] = russian_chars[i]

    return key


def decrypt(text, key):
    """
    Дешифрует текст по ключу
    """
    result = ''
    for char in text:
        result += key.get(char, char)
    return result


def save_key(key, filename):
    """
    Сохраняет ключ в файл
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for k, v in sorted(key.items()):
            f.write(f"{k} -> {v}\n")


def main():

    cipher_text = load_text('input.txt')

    text_freq = analyze_frequency(cipher_text)
    print("Частоты сохранены в freq.txt")

    key = build_key(text_freq)
    save_key(key, 'key.txt')
    print("Ключ сохранен в key.txt")

    decrypted = decrypt(cipher_text, key)
    save_text('decrypted_text.txt', decrypted)
    print("Первичная дефишровка текста сохранена в decrypted_text.txt")


if __name__ == "__main__":
    main()
