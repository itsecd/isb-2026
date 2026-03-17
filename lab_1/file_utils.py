def read_text_from_file(filename):
    """Читает текст из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ОШИБКА: Файл {filename} не найден!")
        return None
    except Exception as e:
        print(f"ОШИБКА при чтении файла {filename}: {e}")
        return None


def save_text(text, filename):
    """Сохраняет текст в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"  {filename}")


def save_key(keyword, filename):
    """Сохраняет ключевое слово в файл"""
    from transposition import get_column_order_from_key

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Ключевое слово: {keyword}\n")
        f.write(f"Длина ключа: {len(keyword)}\n")
        f.write(f"Порядок столбцов: {get_column_order_from_key(keyword)}\n")
    print(f"  {filename}")


def save_frequency_analysis(frequencies, filename):
    """Сохраняет частотный анализ в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Частотный анализ текста\n")
        f.write("Символ | Кол-во | Частота\n")
        for char, count, freq in frequencies:
            if char == ' ':
                display = '(пробел)'
            elif char == '\n':
                display = '(перенос)'
            else:
                display = char
            f.write(f"  {display:7} | {count:6} | {freq:.6f}\n")
    print(f"  {filename}")