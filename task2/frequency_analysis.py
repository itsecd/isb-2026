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


def save_frequencies_to_file(frequencies: dict[str, float], filename: str = "frequencies.txt") -> None:
    """
    Сохранение частот символов в файл.
    
    Args:
        frequencies: словарь с частотами символов
        filename: имя файла для сохранения
    """
    lines = ["Частоты символов в зашифрованном тексте:\n"]
    lines.append("-" * 35)
    lines.append(f"{'Символ':<10} | {'Частота':<12}")
    lines.append("-" * 35)
    
    for ch, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
        display_char = ch if ch.isprintable() else f"\\x{ord(ch):02x}"
        lines.append(f"  {display_char:<8} | {freq:.6f}")
    
    lines.append("-" * 35)
    write_file(filename, "\n".join(lines))
    

def main():

    cipher_text = read_file("cod5.txt")
    print(f"Длина текста: {len(cipher_text)} символов")

    freq = calc_frequency(cipher_text)
    save_frequencies_to_file(freq, "frequencies.txt")

    plain_text = ''.join(key.get(ch, ch) for ch in cipher_text)
    
    output_filename = "decrypted_text.txt"
    save_decrypted_text(output_filename, plain_text)
    

if __name__ == "__main__":
    main()