from const import (
    LOWER_ALPHABET, UPPER_ALPHABET, ALPHABET_LENGTH,
    INPUT_FILENAME, ENCRYPTED_FILENAME, KEY

)

def read_text_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def save_to_file(text, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"✓ Текст сохранён в файл: {filename}")
        return True
    except Exception as e:
        print(f"✗ Ошибка при сохранении файла {filename}: {e}")
        return False
    
def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return ''.join(key)

def get_pos(char):
    if char in LOWER_ALPHABET:
        return LOWER_ALPHABET.index(char)
    elif char in UPPER_ALPHABET:
        return UPPER_ALPHABET.index(char)
    else:
        return -1

def get_char_by_pos(pos, is_upper):
    if is_upper:
        return UPPER_ALPHABET[pos % ALPHABET_LENGTH]
    else:
        return LOWER_ALPHABET[pos % ALPHABET_LENGTH]


def encrypt(text, key):
    encrypted_text = []
    key = generate_key(text, key)
    
    for i in range(len(text)):
        char = text[i]
        pos = get_pos(char)
        
        if pos != -1:
            is_upper = char.isupper()
            key_pos = get_pos(key[i])
            encrypted_pos = (pos + key_pos) % 33
            encrypted_char = get_char_by_pos(encrypted_pos, is_upper)
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)

def decrypt(encrypted_text, key):
    decrypted_text = []
    key = generate_key(encrypted_text, key)
    
    for i in range(len(encrypted_text)):
        char = encrypted_text[i]
        pos = get_pos(char)
        
        if pos != -1: 
            is_upper = char.isupper()
            key_pos = get_pos(key[i])

            decrypted_pos = (pos - key_pos + 33) % 33
            decrypted_char = get_char_by_pos(decrypted_pos, is_upper)
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

def main():
    original_text = read_text_from_file(INPUT_FILENAME)
    
    print("Исходный текст:")
    print(original_text)
    print(f"\nДлина текста: {len(original_text)} символов")
    print(f"Ключевое слово: {KEY}")
    print(f"Длина ключа: {len(KEY)} символов")
    
    encrypted = encrypt(original_text, KEY)

    print("ЗАШИФРОВАННЫЙ ТЕКСТ:")
    print(encrypted)
    
    save_to_file(encrypted,ENCRYPTED_FILENAME)

    decrypted = decrypt(encrypted, KEY)
    print("ДЕШИФРОВАННЫЙ ТЕКСТ:")
    print(decrypted)
    
    print("ПРОВЕРКА:")
    if original_text == decrypted:
        print("Дешифрованный текст полностью совпадает с исходным.")
    else:
        print("Дешифрованный текст отличается от исходного.")
            
if __name__ == "__main__":
    main()