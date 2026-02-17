def vigenere_encrypt(text, key):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    clean_key = ''
    key = key.lower()
    for char in key:
        if char in alphabet:
            clean_key += char
    
    if not clean_key:
        return "Ошибка: ключ должен содержать буквы русского алфавита"
    
    result = ''
    key_index = 0
    
    for char in text:
        if char in alphabet:
            pos = 0
            while pos < len(alphabet) and alphabet[pos] != char:
                pos += 1
            
            key_pos = 0
            while key_pos < len(alphabet) and alphabet[key_pos] != clean_key[key_index]:
                key_pos += 1
            
            new_pos = (pos + key_pos) % 33
            result += alphabet[new_pos]
            
            key_index = (key_index + 1) % len(clean_key)
            
        elif char in alphabet_upper:
            pos = 0
            while pos < len(alphabet_upper) and alphabet_upper[pos] != char:
                pos += 1
            
            key_pos = 0
            while key_pos < len(alphabet) and alphabet[key_pos] != clean_key[key_index]:
                key_pos += 1
            
            new_pos = (pos + key_pos) % 33
            result += alphabet_upper[new_pos]
            
            key_index = (key_index + 1) % len(clean_key)
        else:
            result += char
    
    return result

def vigenere_decrypt(encrypted_text, key):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    clean_key = ''
    key = key.lower()
    for char in key:
        if char in alphabet:
            clean_key += char
    
    if not clean_key:
        return "Ошибка: ключ должен содержать буквы русского алфавита"
    
    result = ''
    key_index = 0
    
    for char in encrypted_text:
        if char in alphabet:
            pos = 0
            while pos < len(alphabet) and alphabet[pos] != char:
                pos += 1
            
            key_pos = 0
            while key_pos < len(alphabet) and alphabet[key_pos] != clean_key[key_index]:
                key_pos += 1
            
            new_pos = (pos - key_pos) % 33
            result += alphabet[new_pos]
            
            key_index = (key_index + 1) % len(clean_key)
            
        elif char in alphabet_upper:
            pos = 0
            while pos < len(alphabet_upper) and alphabet_upper[pos] != char:
                pos += 1
            
            key_pos = 0
            while key_pos < len(alphabet) and alphabet[key_pos] != clean_key[key_index]:
                key_pos += 1
            
            new_pos = (pos - key_pos) % 33
            result += alphabet_upper[new_pos]
            
            key_index = (key_index + 1) % len(clean_key)
        else:
            result += char
    
    return result

def read_key_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            key = file.read().strip()
            if not key:
                raise ValueError("Файл с ключом пуст")
            return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден!")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла с ключом: {e}")

def main():
    try:
        key = read_key_from_file('key.txt')
        print(f"Ключ прочитан из файла: {key}")
        try:
            with open('input.txt', 'r', encoding='utf-8') as file:
                original_text = file.read()
            print(f"Исходный текст прочитан из файла input.txt")
        except FileNotFoundError:
            print("Ошибка: файл 'input.txt' не найден!")
            return
        except Exception as e:
            print(f"Ошибка при чтении input.txt: {e}")
            return
        
        encrypted = vigenere_encrypt(original_text, key)
        
        try:
            with open('encrypted.txt', 'w', encoding='utf-8') as file:
                file.write(encrypted)
            print("Зашифрованный текст сохранен в файл 'encrypted.txt'")
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")
            return
        
        print("\n" + "="*50)
        print("ЗАШИФРОВАННЫЙ ТЕКСТ:")
        print("="*50)
        print(encrypted)
        print("="*50)
        
        decrypted = vigenere_decrypt(encrypted, key)
        print("\nРАСШИФРОВАННЫЙ ТЕКСТ (для проверки):")
        print("="*50)
        print(decrypted)
        print("="*50)
        
        if decrypted == original_text:
            print("\n✓ Проверка пройдена: расшифрованный текст совпадает с исходным")
        else:
            print("\n✗ Внимание: расшифрованный текст НЕ совпадает с исходным!")
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()