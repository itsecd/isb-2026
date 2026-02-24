from collections import Counter
from task2_key import key


def read_file(filename: str) -> str:
    """Чтение содержимого файла и возврат как строки."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def calc_frequency(text: str) -> dict[str, float]:
    """Вычисление частоты каждого символа в тексте."""
    symbols = [ch for ch in text if ch != '\n']
    counter = Counter(symbols)
    total = sum(counter.values())
    return {ch: cnt / total for ch, cnt in counter.items()}


def main():
    # Чтение зашифрованного текста
    cipher_text = read_file("cod5.txt")

    # Вычисление частот символов
    freq = calc_frequency(cipher_text)

    # Вывод таблицы частот
    print("Символ | Частота")
    print("-----------------")
    for ch, f in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ch}    | {f:.6f}")

    # Расшифровка текста
    plain_text = ''.join(key.get(ch, ch) for ch in cipher_text)
    print(plain_text)

if __name__ == "__main__":
    main()