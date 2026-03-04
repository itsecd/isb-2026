import importlib.util

def get_freq_file(text: str) -> None:
    freq = {}
    total_chars = len(text)
    
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    with open("frequency_of_letters_task_2.txt", "w", encoding="utf-8") as f:
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
    replace_table = load_key_from_python("task_2_key.py")
    
    decoded_text = ''.join(replace_table.get(char, char) for char in text)
    
    with open("cod3_result.txt", "w", encoding="utf-8") as f:
        f.write(decoded_text)
    
    print(f"Расшифровано {len(decoded_text)} символов")


def main() -> None:
    with open("cod3.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"Загружено {len(text)} символов из {"cod3.txt"}")
    
    get_freq_file(text)
    print(f"Частотный анализ сохранен в {"frequency_of_letters_task_2.txt"}")
    
    decode_text(text)
    print(f"Результат сохранен в {"cod3_result.txt"}")


if __name__ == "__main__":
    main()
