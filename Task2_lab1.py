def load_text(filename):
    """Загружает текст из файла(filename (str): путь к файлу с текстом, вернет str: загруженный текст"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке файла {filename}: {e}")

def load_key(filename):
    """Загружает ключ дешифрования из файла(filename (str): путь к файлу с ключом, вернет dict: словарь с ключом дешифрования"""
    key = {}#словарь, ключ значение
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Пропускаем первые две строки (заголовок и разделитель)
        for line in lines[2:]:
            line = line.strip()#удаляет все пробельные символы 
            if line and '->' in line:#проверяет, что строка не пустая
                parts = line.split('->')#split('->') разбивает строку на части по разделителю ->
                if len(parts) == 2:#проверка, что получилось ровно две части А->b
                    k = parts[0].strip().strip("'")#очистка от лишнего
                    v = parts[1].strip().strip("'")
                    key[k] = v
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке ключа: {e}")

def calculate_frequencies(text):
    """Рассчитывает частоту символов в тексте
    text (str): текст для анализа
    вернет dict: словарь с частотами символов"""
    # Убираем пробелы и переводы строк для анализа
    text_without_spaces = text.replace(' ', '').replace('\n', '')
    
    # Подсчитываю количество каждого символа
    char_counts = {}
    for char in text_without_spaces:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1#увелич счетчик на 1
    
    # Вычисляем общее количество символов
    total_chars = len(text_without_spaces)
    
    # Преобразуем в относительные частоты
    frequencies = {}
    for char, count in char_counts.items():
        frequencies[char] = count / total_chars
    
    return frequencies

def decrypt(text, key):
    """Дешифрует текст с использованием ключа
        text (str): зашифрованный текст
        key (dict): словарь с ключом дешифрования, 
        вернет str: расшифрованный текст"""
    result = []
    for line in text.split('\n'):#разбивает исходный текст на отдельные строки по символу
        decrypted_line = ''#создаю пустую строку, куда буду собирать расшифрованные символы
        for char in line:
            if char in key:
                decrypted_line += key[char]
            else:
                decrypted_line += char
        result.append(decrypted_line)
    return '\n'.join(result)

def save_text(filename, text):
    """Сохраняет текст в файл
        filename (str): имя файла для сохранения
        text (str): текст для сохранения"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        raise Exception(f"Ошибка при сохранении текста в {filename}: {e}")

def save_frequencies(filename, frequencies, original_text):
    """Сохраняет результаты анализа частотности в файл
        filename (str): имя файла для сохранения
        frequencies (dict): частоты символов исходного текста (относительные)
        original_text (str): исходный зашифрованный текст"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Анализ частотности символов в тексте\n")
                        
            sorted_chars = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)# Сортирую по убыванию частоты
            
            for char, freq in sorted_chars:
                f.write(f"'{char}': {freq:.6f}\n")
            
            # Вычисляю общее количество символов из исходного текста (без пробелов)
            text_without_spaces = original_text.replace(' ', '').replace('\n', '')
            total_chars = len(text_without_spaces)
            f.write(f"Всего символов (без пробелов): {total_chars}\n")
            f.write(f"Уникальных символов: {len(frequencies)}\n")
    except Exception as e:
        raise Exception(f"Ошибка при сохранении частот: {e}")

def main():
    try:
        print("Дешефрирование текста и анализ частотности")
        
        original_text = load_text('Task2_original_text.txt')
        
        key = load_key('Text2_key.txt')
        
        frequencies = calculate_frequencies(original_text)
        
        decrypted_text = decrypt(original_text, key)
        
        save_text('Task2_decrypted_text.txt', decrypted_text)
        save_frequencies('Task2_frequency_analysis.txt', frequencies, original_text)
                
        print("\nПервые 121 символов расшифрованного текста:")
        print(decrypted_text[:121] + "...")
        
        print("Дешифрование успешно завершено!")
        
    except Exception as e:
        print(f"\n Ошибка: {e}")

if __name__ == "__main__":
    main()