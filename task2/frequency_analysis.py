from collections import Counter
from key import key


def read_file(filename: str) -> str:
    """Чтение содержимого файла и возврат как строки."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename: str, text: str) -> None:
    """Запись текста в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def calc_frequency(text: str) -> dict[str, float]:
    """Вычисление частоты каждого символа в тексте."""
    symbols = [ch for ch in text if ch != '\n']
    counter = Counter(symbols)
    total = sum(counter.values())
    return {ch: cnt / total for ch, cnt in counter.items()}


def save_decrypted_text(filename: str, text: str) -> None:
    """
    Сохранение расшифрованного текста в файл.
    
    Args:
        filename: имя файла для сохранения
        text: расшифрованный текст
    """
    write_file(filename, text)
    print(f"\nРасшифрованный текст сохранён в файл: {filename}")


def main():

    cipher_text = read_file("cod5.txt")
    print(f"Длина текста: {len(cipher_text)} символов")

    # Вычисление частот символов
    freq = calc_frequency(cipher_text)

    print("-" * 30)
    print(f"{'Символ':<8} | {'Частота':<10}")
    print("-" * 30)
    for ch, f in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        display_char = ch if ch.isprintable() else f"\\x{ord(ch):02x}"
        print(f"  {display_char:<6} | {f:.6f}")
    print("-" * 30)

    plain_text = ''.join(key.get(ch, ch) for ch in cipher_text)
    
    output_filename = "decrypted_text.txt"
    save_decrypted_text(output_filename, plain_text)
    

if __name__ == "__main__":
    main()