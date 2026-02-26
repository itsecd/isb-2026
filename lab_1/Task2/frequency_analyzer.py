import json

from files import KEY_FILE, DECODE_FILE, INPUT_FILE, FREQ_FILE


SPECIAL_CHARS = {
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    ' ': 'пробел'
}

def freq_file(text: str) -> None:
    """Выполняет частотный анализ символов в тексте и сохраняет результаты в файл"""
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
            for char, count in sorted_freq:
    
                if char in SPECIAL_CHARS:
                    display = SPECIAL_CHARS[char]
                else:
                    display = char
                frequency = count / total_chars
                f.write(f"{display} {frequency:.6f}\n")
    except IOError as e:
        raise IOError(f"Не удалось записать файл с частотным анализом: {e}")

def decode(text: str) -> None:
    """Дешифрует текст используя JSON файл с ключом и сохраняет результат с переносом строк."""
    try:
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            key = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с ключом {KEY_FILE} не найден")
    except json.JSONDecodeError as e:
        raise ValueError(f"Неверный JSON в файле с ключом: {e}")
    
    if not isinstance(key, dict):
        raise TypeError("Ключ должен быть словарем")
    
    decoded_text = ""
    for char in text:
        if char in key:
            if not isinstance(key[char], str):
                raise TypeError(f"Значение ключа для '{char}' должно быть строкой")
            decoded_text += key[char]
        else:
            decoded_text += char

    formatted_text = ""
    for i in range(0, len(decoded_text), 90):
        formatted_text += decoded_text[i:i+90] + "\n"

    try:
        with open(DECODE_FILE, "w", encoding="utf-8") as f:
            f.write(formatted_text)
    except IOError as e:
        raise IOError(f"Не удалось записать файл с расшифрованным текстом: {e}")


def main() -> None:
    """Главная функция для организации частотного анализа и дешифровки."""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Входной файл {INPUT_FILE} не найден")
    except IOError as e:
        raise IOError(f"Не удалось прочитать входной файл: {e}")
    
    if not text:
        raise ValueError("Входной файл пуст")
    
    freq_file(text)
    decode(text)


if __name__ == "__main__":
    main()
