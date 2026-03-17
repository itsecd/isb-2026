import argparse
from collections import Counter
import sys


def read_encrypted(filename):
    """Читает зашифрованный текст из файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        sys.exit(1)


def count_frequencies(text):
    """Возвращает словарь частот символов в тексте."""
    return Counter(text)


def get_count(item):
    """Вспомогательная функция для сортировки по частоте (второй элемент кортежа)."""
    return item[1]


def write_frequencies(freq_dict, filename, total):
    """Записывает частоты символов в файл (по убыванию частоты)."""
    if total == 0:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Текст пуст, нет символов для анализа.\n")
            return
        except Exception as e:
            print(f"Ошибка при записи файла частот {filename}: {e}")
            sys.exit(1)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            sorted_items = sorted(freq_dict.items(), key=get_count, reverse=True)
            for char, count in sorted_items:
                if char == ' ':
                    display = 'пробел'
                else:
                    display = char

                percentage = (count / total) * 100
                f.write(f"{display}: {count} ({percentage:.1f}%)\n")
    except Exception as e:
        print(f"Ошибка при записи файла частот {filename}: {e}")
        sys.exit(1)


def parse_key_line(line):
    """
    Разбирает строку с ключами вида "М= ,>=и,Е=с,1=о,r=т".
    Возвращает словарь {зашифрованный_символ: расшифрованный_символ}.
    """
    key_dict = {}
    parts = line.strip().split(',')
    for part in parts:
        if not part:
            continue
        if '=' not in part:
            print(f"Предупреждение: пропущен некорректный фрагмент '{part}' (нет '=')")
            continue
        left, right = part.split('=', 1)
        if right == '' and left != '':
            print(f"Предупреждение: для символа '{left}' не указано соответствие, пропускаем.")
            continue
        if left == '':
            print(f"Предупреждение: пустой шифрованный символ в '{part}', пропускаем.")
            continue
        key_dict[left] = right
    return key_dict


def read_key(filename):
    """Читает файл ключей и возвращает словарь замены."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = ' '.join(line.strip() for line in f)
            return parse_key_line(content)
    except FileNotFoundError:
        print(f"Ошибка: файл ключей {filename} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла ключей {filename}: {e}")
        sys.exit(1)


def decrypt(text, key_dict):
    """
    Применяет замену к тексту.
    Если символ отсутствует в словаре, он остаётся без изменений.
    """
    return ''.join(key_dict.get(ch, ch) for ch in text)


def write_decrypted(text, filename):
    """Записывает расшифрованный текст в файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(f"Ошибка при записи расшифрованного файла {filename}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Дешифровка сообщения, закодированного моноалфавитной заменой.")
    parser.add_argument('encrypted_file', help='файл с зашифрованным текстом')
    parser.add_argument('key_file', help='файл с ключами замены')
    parser.add_argument('output_file', help='файл для записи расшифрованного текста')
    parser.add_argument('freq_file', help='файл для записи частот символов')
    args = parser.parse_args()

    encrypted_text = read_encrypted(args.encrypted_file)
    total_chars = len(encrypted_text)
    freq = count_frequencies(encrypted_text)
    write_frequencies(freq, args.freq_file, total_chars)
    print(f"Частоты символов записаны в {args.freq_file}")

    key_dict = read_key(args.key_file)
    if not key_dict:
        print("Предупреждение: словарь ключей пуст. Расшифровка не изменит текст.")
    else:
        print(f"Загружено {len(key_dict)} замен.")

    decrypted_text = decrypt(encrypted_text, key_dict)

    write_decrypted(decrypted_text, args.output_file)
    print(f"Расшифрованный текст записан в {args.output_file}")


if __name__ == "__main__":
    main()
