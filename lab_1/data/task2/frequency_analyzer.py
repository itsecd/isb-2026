import json
from files import KEY_FILE, DECODE_FILE, INPUT_FILE, FREQ_FILE

SPECIAL_CHARS = {
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    ' ': 'пробел'
}

def freq_file(text: str) -> None:
    """Выполняет частотный анализ символов в тексте"""
    print("Выполняется частотный анализ...")
    freq = {}
    total_chars = 0
    
    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
        total_chars += 1

    if total_chars == 0:
        raise ValueError("Входной текст пуст")

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    try:
        with open(FREQ_FILE, "w", encoding="utf-8") as f:
            f.write("Символ | Частота | Процент\n")
            f.write("-" * 30 + "\n")
            for char, count in sorted_freq:
                if char in SPECIAL_CHARS:
                    display = SPECIAL_CHARS[char]
                else:
                    display = char
                frequency = count / total_chars
                f.write(f"{display:6} | {count:5}   | {frequency:.2%}\n")
        print(f"Таблица частот сохранена в {FREQ_FILE}")
    except IOError as e:
        raise IOError(f"Не удалось записать файл: {e}")

def decode(text: str) -> None:
    """Дешифрует текст используя JSON файл с ключом"""
    print("Загрузка ключа...")
    try:
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            key = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с ключом {KEY_FILE} не найден")
    except json.JSONDecodeError as e:
        raise ValueError(f"Неверный JSON в файле с ключом: {e}")
    
    if not isinstance(key, dict):
        raise TypeError("Ключ должен быть словарем")

    print("Дешифровка текста...")
    decoded_text = ""
    
    for char in text:
        if char in key:
            decoded_text += key[char]
        else:
            decoded_text += char

    formatted_text = ""
    for i in range(0, len(decoded_text), 90):
        formatted_text += decoded_text[i:i+90] + "\n"

    try:
        with open(DECODE_FILE, "w", encoding="utf-8") as f:
            f.write(formatted_text)
        print(f"Результат сохранен в {DECODE_FILE}")
    except IOError as e:
        raise IOError(f"Не удалось записать файл: {e}")

def main() -> None:
    """Главная функция"""
    print("Начало работы программы")
    print(f"Чтение файла {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"Файл загружен, размер: {len(text)} символов")
    except FileNotFoundError:
        raise FileNotFoundError(f"Входной файл {INPUT_FILE} не найден")
    except IOError as e:
        raise IOError(f"Не удалось прочитать входной файл: {e}")

    if not text:
        raise ValueError("Входной файл пуст")

    freq_file(text)
    decode(text)
    print("Программа завершена")


if __name__ == "__main__":
    main()