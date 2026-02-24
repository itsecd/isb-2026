DECRYPT_MODE = False
KEY_FILE = 'd:/Учеба/Лабы/ОИБ/lab1/key.txt'
INPUT_FILE = 'd:/Учеба/Лабы/ОИБ/lab1/input2.txt' 
OUTPUT_FILE = 'd:/Учеба/Лабы/ОИБ/lab1/output2.txt'
def load_key(key_file):
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


def encrypt(text, key_map):
    """Шифрует текст"""
    return ''.join(key_map.get(char, char) for char in text)


def decrypt(text, reverse_key_map):
    """Дешифрует текст"""
    return ''.join(reverse_key_map.get(char, char) for char in text)


def main():
    key_map, reverse_key_map = load_key(KEY_FILE)
    print(f"Ключ загружен: {len(key_map)} пар символов")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"Входной файл прочитан: {len(text)} символов")
    
    if DECRYPT_MODE:
        result = decrypt(text, reverse_key_map)
        print("Режим: ДЕШИФРОВАНИЕ")
    else:
        result = encrypt(text, key_map)
        print("Режим: ШИФРОВАНИЕ")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"Результат сохранён в '{OUTPUT_FILE}'")
    print("\nГотово!")


if __name__ == '__main__':
    main()