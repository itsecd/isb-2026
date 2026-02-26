
def load_polybius_square(filename):
    """Загружает квадрат Полибия из файла
    (filename (str): путь к файлу с квадратом Полибия), вернет:
    list: двумерный список, представляющий квадрат Полибия """
    square = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                row = line.strip().split()                     #line.strip() — удаляет все лишние пробелы и символы переноса строки
                if len(row) != 6:                              #.split() — разбивает строку на части по пробелам и возвращает список
                    raise ValueError(f"Строка {line_num} должна содержать 6 символов")
                square.append(row)#добавляем строку в конец этого списка
        
        if len(square) != 6:
            raise ValueError("Квадрат Полибия должен содержать 6 строк")
        
        return square
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке квадрата Полибия: {e}")

def load_text(filename):
    """Загружает текст из файла(filename (str): путь к файлу с текстом), вернет str: загруженный текст"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")

def encryption(text, polybius_square):
    """Шифрует текст с использованием квадрата Полибия(text (str): исходный текст для шифрования polybius_square (list): квадрат Полибия)
       вернет str: зашифрованный текст в виде строки чисел"""
    text = text.upper()
    result = []
    
    for char in text:
        if char == ' ':
            result.append('68')
            continue
            
        found = False
        for row in range(6):
            for col in range(6):
                if polybius_square[row][col] == char:
                    result.append(str(row + 1) + str(col + 1))
                    found = True
                    break
            if found:
                break
        
        if not found and char != '\n':
            print(f"Предупреждение: символ '{char}' не найден в квадрате Полибия")
    
    return ' '.join(result)#объединяет через пробел

def decryption(encrypted_text, polybius_square):
    """Дешифрует текст из числового представления обратно в символы(encrypted_text (str): зашифрованный текст в виде строки чисел
        polybius_square (list): квадрат Полибия), вернет str: расшифрованный текст"""
   
    codes = encrypted_text.split()#split() разбивает строку на список13 24 35->['13', '24', '35']
    result = []
    
    for code in codes:
        if code == '68':
            result.append(' ')
            continue
            
        row = int(code[0]) - 1#code[0] — первый символ строки (например, '1'
        col = int(code[1]) - 1#code[1] — второй символ строки (например, '3'
        
        if 0 <= row < 6 and 0 <= col < 6:
            result.append(polybius_square[row][col])
        else:
            result.append('?')
    
    return ''.join(result)#объединяет через пробел

def save_key_info(filename, polybius_square):
    """Сохраняет информацию о ключе шифрования в файл(filename (str): имя файла для сохранения, polybius_square (list): квадрат Полибия)"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Квадрат Полибия (ключ шифрования):\n")
            f.write("   1 2 3 4 5 6\n")
            for i, row in enumerate(polybius_square, 1):#проходит по всем строкам квадрата начиная с 1 строки
                f.write(f"{i}  {' '.join(row)}\n")
    except Exception as e:
        raise Exception(f"Ошибка при сохранении ключа: {e}")

def save_text(filename, text):
    """Сохраняет текст в файл(filename (str): имя файла для сохранения, text (str): текст для сохранения"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        raise Exception(f"Ошибка при сохранении текста в {filename}: {e}")

def main():
    try:
        polybius_square = load_polybius_square('key.txt')
        
        text = load_text('Task1_original_text.txt')
        
        print("Работа квадрата Полибия")

        encrypted_text = encryption(text, polybius_square)
        
        decrypted_text = decryption(encrypted_text, polybius_square)
        
        print("\n1. Исходный текст (первые 121 символов):")
        print(text[:121] + "...")
        
        print("\n2. Зашифрованный текст (первые 21 чисел):")
        print(encrypted_text[:21] + "...")
        
        print("\n3. Расшифрованный текст (первые 121 символов):")
        print(decrypted_text[:121] + "...")
        
        save_text('Task1_encrypted_text.txt', encrypted_text)
        save_key_info('Task1_encryption_key.txt', polybius_square)
        
        print("\nШифрование успешно завершено")
        print("Файлы сохранены:")
        print("- Task1_encrypted_text.txt (зашифрованный текст)")
        print("- Task1_encryption_key.txt (ключ шифрования)")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()