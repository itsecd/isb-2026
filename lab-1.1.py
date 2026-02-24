def create_atbash_mapping():
    """Создаёт словарь подстановки для шифра Атбаш (русский алфавит)"""
    alphabet = 'абвгде жзийклмнопрстуфхцчшщъыьэюя'
    reversed_alphabet = alphabet[::-1]
    
    mapping = {}
    for orig, subst in zip(alphabet, reversed_alphabet):
        mapping[orig] = subst
        mapping[orig.upper()] = subst.upper()
    
    return mapping

def encrypt_atbash(text, mapping):
    """Шифрует текст с помощью шифра Атбаш"""
    return ''.join(mapping.get(char, char) for char in text)

def decrypt_atbash(text, mapping):
    """Расшифровывает текст (для Атбаш процесс идентичен шифрованию)"""
    return encrypt_atbash(text, mapping)

def process_file(input_file, output_file, mode='encrypt'):
    """Обрабатывает файл: шифрует или расшифровывает"""
    mapping = create_atbash_mapping()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if mode == 'encrypt':
            processed = encrypt_atbash(content, mapping)
        else:
            processed = decrypt_atbash(content, mapping)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed)
        
        print(f"Успешно: {mode} '{input_file}' → '{output_file}'")
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_file}' не найден")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    # Пример использования
    #process_file('D:\Учеба\Лабы\ОИБ\lab1\lab-1.1_text.txt', 'D:\Учеба\Лабы\ОИБ\lab1\encrypted.txt', mode='encrypt')
    # Для расшифровки:
    process_file('D:\Учеба\Лабы\ОИБ\lab1\encrypted.txt', 'D:\Учеба\Лабы\ОИБ\lab1\decrypted.txt', mode='decrypt')