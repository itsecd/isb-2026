import collections
from config import DECRYPT_MODE, KEY_FILE, INPUT_FILE, OUTPUT_FILE
def show_frequences() -> None:
    total = len(INPUT_FILE)
    counter = collections.Counter(INPUT_FILE)

    print(f"{'Символ':<10} | {'Количество':<10} | {'Процент':<10}")
    print("-" * 35)

    for char, count in counter.most_common():
        percent = (count / total) * 100
        display_char = repr(char)[1:-1] if char in [' ', '\n', '\t'] else char
        print(f"{display_char:<10} | {count:<10} | {percent:>6.2f}%")
def load_key(key_file) -> dict:
    """Загружает ключ шифрования из файла"""
    key_map = {}
    reverse_key_map = {}
    
    with open(key_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line:
                continue
            
            parts = line.split('-')
            if len(parts) != 2:
                continue
            
            cipher_char = parts[0].strip()
            plain_char = parts[1].strip().strip("'\"")
            
            key_map[cipher_char] = plain_char
            reverse_key_map[plain_char] = cipher_char
    
    return key_map, reverse_key_map


def encrypt(text, key_map) -> str:
    """Шифрует текст"""
    return ''.join(key_map.get(char, char) for char in text)

def main() -> None:
    key_map, reverse_key_map = load_key(KEY_FILE)
    print(f"Ключ загружен: {len(key_map)} пар символов")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"Входной файл прочитан: {len(text)} символов")
    
    if DECRYPT_MODE:
        result = encrypt(text, reverse_key_map)
        print("Режим: ДЕШИФРОВАНИЕ")
    else:
        result = encrypt(text, key_map)
        print("Режим: ШИФРОВАНИЕ")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"Результат сохранён в '{OUTPUT_FILE}'")
    print("\nГотово!")
    show_frequences()

if __name__ == '__main__':
    main()

