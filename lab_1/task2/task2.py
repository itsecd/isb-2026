import importlib.util

from const_task2 import KEY_FILE, DECODE_FILE, INPUT_FILE, FREQ_FILE


def get_freq_file(text: str) -> None:
    freq = {}
    total_chars = len(text)
    
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    with open(FREQ_FILE, "w", encoding="utf-8") as f:
        f.write(f"Всего символов: {total_chars}\n\n")
        for char, count in sorted_freq:
            percentage = (count / total_chars) * 100
            f.write(f"{repr(char)}: {count} ({percentage:.2f}%)\n")


def load_key_from_python(filepath: str) -> dict:
    spec = importlib.util.spec_from_file_location("key_module", filepath)
    key_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(key_module)
    return key_module.KEY


def decode_text(text: str) -> None:
    replace_table = load_key_from_python(KEY_FILE)
    
    decoded_text = ''.join(replace_table.get(char, char) for char in text)
    
    with open(DECODE_FILE, "w", encoding="utf-8") as f:
        f.write(decoded_text)
    
    print(f"Расшифровано {len(decoded_text)} символов")


def main() -> None:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"Загружено {len(text)} символов из {INPUT_FILE}")
    
    get_freq_file(text)
    print(f"Частотный анализ сохранен в {FREQ_FILE}")
    
    decode_text(text)
    print(f"Результат сохранен в {DECODE_FILE}")


if __name__ == "__main__":
    main()