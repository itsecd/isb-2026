import ru_freq
from collections import Counter
import config 


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

    freq = Counter(text_plain)

    items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    with open(config.FREQ_FILE, 'w', encoding='utf-8') as f:
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
    cipher_text = load_text(config.INPUT_FILE)

    text_freq = analyze_frequency(cipher_text)
    print(f"Частоты сохранены в {config.FREQ_FILE}")

    key = build_key(text_freq)
    save_key(key, config.KEY_FILE)
    print(f"Ключ сохранен в {config.KEY_FILE}")

    decrypted = decrypt(cipher_text, key)
    save_text(config.DECRYPTED_TEXT_FILE, decrypted)
    print(f"Первичная дешифровка текста сохранена в {config.DECRYPTED_TEXT_FILE}")


if __name__ == "__main__":
    main()
