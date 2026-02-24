from collections import Counter

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
    key = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Пропускаем первые две строки (заголовок и разделитель)
        for line in lines[2:]:
            line = line.strip()
            if line and '->' in line:
                parts = line.split('->')
                if len(parts) == 2:
                    k = parts[0].strip().strip("'")
                    v = parts[1].strip().strip("'")
                    key[k] = v
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке ключа: {e}")

def calculate_frequencies(text):
    """Рассчитывает частоту символов в тексте(text (str): текст для анализа, 
    вернет Counter: объект Counter с частотами символов (без пробелов и переводов строк)"""
    # Убираем пробелы и переводы строк для анализа
    text_without_spaces = text.replace(' ', '').replace('\n', '')
    return Counter(text_without_spaces)

def decrypt(text, key):
    """Дешифрует текст с использованием ключа
        text (str): зашифрованный текст
        key (dict): словарь с ключом дешифрования, 
        вернет str: расшифрованный текст"""
    result = []
    for line in text.split('\n'):
        decrypted_line = ''
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
    """Сохраняет результаты анализа частотности в файл(
        filename (str): имя файла для сохранения
        frequencies (Counter): частоты символов исходного текста
        original_text (str): исходный зашифрованный текст
        decrypted_text (str): расшифрованный текст)"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Анализ частотности символов в тексте\n")
            
            f.write("Исходный зашифрованный текст (первые 200 символов):\n")
            f.write(original_text[:200] + "...\n\n")
            
            f.write("Частота символов в исходном тексте (без пробелов):\n")
            f.write("-" * 40 + "\n")
            
            # Сортируем по убыванию частоты
            for char, count in frequencies.most_common():
                percentage = (count / sum(frequencies.values())) * 100
                f.write(f"'{char}': {count} раз ({percentage:.2f}%)\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"Всего символов (без пробелов): {sum(frequencies.values())}\n")
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