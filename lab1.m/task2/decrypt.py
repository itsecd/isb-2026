"""Частотный анализ и расшифровка текста."""

from collections import Counter


def read_file(filename: str) -> str:
    """Читает содержимое файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден.")
    except Exception as e:
        raise IOError(f"Ошибка при чтении файла '{filename}': {e}")


def write_file(filename: str, content: str) -> None:
    """Записывает содержимое в файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Ошибка при записи файла '{filename}': {e}")


def load_base_frequencies(filename: str) -> dict:
    """Загружает базовые частоты букв из файла."""
    base = {}
    content = read_file(filename)
    
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if ' = ' not in line:
            continue
        letter_part, freq_part = line.split(' = ', 1)
        letter = letter_part.strip()
        freq = float(freq_part.strip())
        base[letter] = freq
    return base

def count_frequencies(text: str) -> Counter:
    """Подсчитывает абсолютную частоту символов."""
    return Counter(text)


def frequencies_to_relative(freq: Counter, total: int) -> dict:
    """Преобразует абсолютные частоты в относительные (десятичные)."""
    return {ch: count / total for ch, count in freq.items()}


def save_frequencies(freq: dict, filename: str) -> None:
    """Сохраняет частоты в файл (отсортированные по убыванию)."""
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    lines = ["Символ | Частота"]
    lines.append("-------|-------------------")
    for ch, value in sorted_items:
        if ch == ' ':
            display = 'пробел'
        elif ch == '\n':
            display = '\\n'
        else:
            display = ch
        lines.append(f"{display:6} | {value:.6f}")
    write_file(filename, '\n'.join(lines))


def compare_frequencies(text_freq: dict, base_freq: dict, output_file: str) -> None:
    """Сравнивает частоты текста с базовыми и выводит таблицу соответствия."""
    sorted_text = sorted(text_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_base = sorted(base_freq.items(), key=lambda x: x[1], reverse=True)

    lines = ["Предполагаемое соответствие символ -> буква"]
    lines.append("Символ (в тексте) | Частота (текст) | Буква (базовая) | Частота (базовая)")
    lines.append("------------------|------------------|-----------------|-------------------")

    for i in range(min(len(sorted_text), len(sorted_base))):
        text_char, text_f = sorted_text[i]
        base_char, base_f = sorted_base[i]

        text_display = 'пробел' if text_char == ' ' else ('\\n' if text_char == '\n' else text_char)
        base_display = 'пробел' if base_char == ' ' else base_char

        lines.append(f"{text_display:16} | {text_f:.6f}        | {base_display:15} | {base_f:.6f}")

    write_file(output_file, '\n'.join(lines))


def load_key(key_file: str) -> dict:
    """Загружает ключ расшифровки из файла."""
    key = {}
    content = read_file(key_file)
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ' - ' not in line:
            continue
        symbol, letter = line.split(' - ', 1)
        if letter == 'пробел':
            letter = ' '
        key[symbol] = letter
    return key


def decrypt(text: str, key: dict) -> str:
    """Расшифровывает текст, заменяя символы по ключу."""
    result = []
    for ch in text:
        if ch == '\n':
            result.append('\n')
        else:
            result.append(key.get(ch, ch))
    return ''.join(result)


def main() -> None:
    """Основная функция."""
    try:
        encrypted_file = 'cod9.txt'
        base_file = 'base_frequencies.txt'
        freq_file = 'frequencies.txt'
        comparison_file = 'comparison.txt'
        key_file = 'key.txt'
        output_file = 'decrypted.txt'

        print(f"Чтение зашифрованного текста из '{encrypted_file}'...")
        encrypted = read_file(encrypted_file)

        print("Подсчёт частот...")
        abs_freq = count_frequencies(encrypted)
        total = len(encrypted)
        rel_freq = frequencies_to_relative(abs_freq, total)

        print(f"Сохранение частот в '{freq_file}'...")
        save_frequencies(rel_freq, freq_file)

        print(f"Загрузка базовых частот из '{base_file}'...")
        base = load_base_frequencies(base_file)

        print(f"Сравнение с базовыми частотами -> '{comparison_file}'...")
        compare_frequencies(rel_freq, base, comparison_file)

        print(f"Загрузка ключа из '{key_file}'...")
        key = load_key(key_file)

        print("Расшифровка...")
        decrypted = decrypt(encrypted, key)

        print(f"Сохранение результата в '{output_file}'...")
        write_file(output_file, decrypted)

        print("Готово.")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()