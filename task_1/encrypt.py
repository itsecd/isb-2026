import json
import os

SIZE = 6  # так как 36 ячеек

def read_key_txt(filename):
    """Читает квадрат Полибия из текстового файла и создает маппинг для JSON."""
    if not os.path.exists(filename):
        print(f"Ошибка: файл {filename} не найден!")
        return None, None
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    square = []
    for line in lines[1:]:
        line = line.rstrip('\n')
        if line:
            chars = line[4:].split('   ')
            square.append(chars)
    
    if len(square) != SIZE:
        print(f"Ошибка: в файле {len(square)} строк, ожидалось {SIZE}")
        return None, None
    
    encrypt_map = {}
    alphabet = ""
    
    for i in range(SIZE):
        if len(square[i]) != SIZE:
            print(f"Ошибка: в строке {i+1} {len(square[i])} элементов, ожидалось {SIZE}")
            return None, None
        
        for j in range(SIZE):
            char = square[i][j]
            if char != '*':
                if char == '_':
                    encrypt_map[' '] = f"{i+1:01d}{j+1:01d}"
                    alphabet += ' '
                else:
                    encrypt_map[char] = f"{i+1:01d}{j+1:01d}"
                    alphabet += char
    
    return encrypt_map, alphabet

def save_key_json(filename, encrypt_map):
    """Сохраняет маппинг в JSON формате."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(encrypt_map, f, ensure_ascii=False, indent=2)

def encrypt_polybius(text, encrypt_map):
    """Шифрует текст, заменяя символы на координаты."""
    encrypted_pairs = []
    unknown_chars = set()
    
    for char in text:
        if char in encrypt_map:
            encrypted_pairs.append(encrypt_map[char])
        else:
            unknown_chars.add(char)
            encrypted_pairs.append('??')
    
    if unknown_chars:
        print(f"Предупреждение: следующие символы не найдены в ключе: {sorted(unknown_chars)}")
    
    return ' '.join(encrypted_pairs)

def decrypt_polybius(encrypted_text, encrypt_map):
    """Дешифрует текст из координат обратно в буквы."""
    decrypt_map = {v: k for k, v in encrypt_map.items()}
    
    pairs = encrypted_text.split(' ')
    decrypted_text = []
    unknown_pairs = set()
    
    for pair in pairs:
        if pair in decrypt_map:
            decrypted_text.append(decrypt_map[pair])
        else:
            unknown_pairs.add(pair)
            decrypted_text.append('?')
    
    if unknown_pairs:
        print(f"Следующие координаты не найдены в ключе: {sorted(unknown_pairs)}")
    
    return ''.join(decrypted_text)

def save_to_file(filename, content):
    """Сохраняет содержимое в файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def print_key_preview(filename):
    """Выводит содержимое key.txt для наглядности."""
    print("\nИспользуемый ключ шифрования (key.txt):")
    with open(filename, 'r', encoding='utf-8') as f:
        print(f.read())

if not os.path.exists('key.txt'):
    print("\nФайл key.txt не найден!")
    exit(1)

print("\nЧтение ключа из key.txt.")
encrypt_map, alphabet = read_key_txt('key.txt')

if encrypt_map is None:
    print("Ошибка при чтении key.txt. Проверьте формат файла.")
    exit(1)

print(f"Ключ успешно загружен!")
print(f"Найдено символов в ключе: {len(encrypt_map)}")
print(f"Алфавит из ключа: {alphabet}")

print("Создание key.json на основе key.txt.")
save_key_json('key.json', encrypt_map)

print_key_preview('key.txt')

original_text = """КРИПТОГРАФИЯ ЭТО НАУКА О МЕТОДАХ ОБЕСПЕЧЕНИЯ КОНФИДЕНЦИАЛЬНОСТИ И АУТЕНТИЧНОСТИ ИНФОРМАЦИИ ИСТОРИЯ КРИПТОГРАФИИ НАСЧИТЫВАЕТ НЕСКОЛЬКО ТЫСЯЧЕЛЕТИЙ ОДНИМ ИЗ ПЕРВЫХ ИЗВЕСТНЫХ ПРИМЕРОВ ЯВЛЯЕТСЯ ЕГИПЕТСКИЙ ИЕРОГЛИФИЧЕСКИЙ ТЕКСТ ДАТИРУЕМЫЙ ОКОЛО ТЫСЯЧИ ДЕВЯТИСОТОГО ГОДА ДО НАШЕЙ ЭРЫ В ДРЕВНЕЙ ГРЕЦИИ ПРИМЕНЯЛСЯ ШИФР СКИТАЛА ИСПОЛЬЗОВАВШИЙ ЦИЛИНДР ОПРЕДЕЛЕННОГО ДИАМЕТРА ДЛЯ ШИФРОВАНИЯ ТЕКСТА ИЗВЕСТНЫЙ РИМСКИЙ ПОЛКОВОДЕЦ ЮЛИЙ ЦЕЗАРЬ ИСПОЛЬЗОВАЛ ШИФР ПРОСТОЙ ПОДСТАНОВКИ КОТОРЫЙ ТЕПЕРЬ НАЗЫВАЕТСЯ ШИФРОМ ЦЕЗАРЯ В ЭПОХУ ВОЗРОЖДЕНИЯ ПОЯВИЛИСЬ БОЛЕЕ СЛОЖНЫЕ МЕТОДЫ ШИФРОВАНИЯ В ДВАДЦАТОМ ВЕКЕ РАЗВИТИЕ ЭЛЕКТРОННЫХ ВЫЧИСЛИТЕЛЬНЫХ МАШИН ПРИВЕЛО К ПОЯВЛЕНИЮ НОВЫХ КРИПТОГРАФИЧЕСКИХ АЛГОРИТМОВ И СОВРЕМЕННЫХ МЕТОДОВ ЗАЩИТЫ ИНФОРМАЦИИ"""

original_text = original_text.upper()

print("Исходный текст (original.txt):")
print(original_text)
print(f"Длина исходного текста: {len(original_text)} символов\n")

encrypted_text = encrypt_polybius(original_text, encrypt_map)

decrypted_text = decrypt_polybius(encrypted_text, encrypt_map)

save_to_file('original.txt', original_text)
save_to_file('encrypted.txt', encrypted_text)

print("Зашифрованный текст (encrypted.txt):")
print(encrypted_text)
print(f"\nВсего пар координат: {len(encrypted_text.split())}\n")

print("Расшифрованный текст (проверка):")
print(decrypted_text)
print(f"Всего символов: {len(decrypted_text)}\n")

if original_text == decrypted_text:
    print("Шифрование работает корректно.")
else:
    print("Расшифрованный текст не совпадает с оригиналом.")
