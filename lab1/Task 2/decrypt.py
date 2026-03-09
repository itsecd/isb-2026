def load_ciphertext(filename):
    """
    Загружает зашифрованный текст из файла.
    
    Args:
        filename (str): Имя файла с зашифрованным текстом
        
    Returns:
        str: Содержимое файла в верхнем регистре
        
    Raises:
        FileNotFoundError: Если файл не найден
        UnicodeDecodeError: Если возникла ошибка кодировки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().upper()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        raise
    except UnicodeDecodeError:
        print(f"Ошибка: Не удалось прочитать файл '{filename}' - проблема с кодировкой")
        raise

def calculate_frequencies(text):
    """
    Вычисляет частоты символов в тексте.
    
    Args:
        text (str): Анализируемый текст
        
    Returns:
        list: Список кортежей (символ, количество, процент)
              отсортированный по убыванию количества
    """
    freq = {}
    total_chars = len(text)
    
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    
    frequencies = []
    for c, count in freq.items():
        percentage = (count / total_chars) * 100
        frequencies.append((c, count, percentage))
    
    return sorted(frequencies, key=lambda x: x[1], reverse=True)

def display_frequencies(frequencies):
    """
    Выводит таблицу частот символов.
    
    Args:
        frequencies (list): Список частот от calculate_frequencies
    """
    print('Анализ частот символов:')
    print('Символ | Количество | Частота (%)')
    print('-------|------------|------------')
    for c, count, percentage in frequencies[:15]:
        if c == ' ':
            display_char = 'ПРОБЕЛ'
        elif c == '\n':
            display_char = '\\n'
        else:
            display_char = c
        print(f'{display_char:6} | {count:10} | {percentage:6.2f}%')

def save_frequencies_to_file(frequencies):
    """
    Сохраняет результаты частотного анализа в файл.
    
    Args:
        frequencies (list): Список частот от calculate_frequencies
        
    Raises:
        IOError: Если возникла ошибка при записи файла
    """
    try:
        with open('frequencies.txt', 'w', encoding='utf-8') as f:
            f.write('Символ | Количество | Частота (%)\n')
            f.write('-------|------------|------------\n')
            for c, count, percentage in frequencies:
                if c == ' ':
                    display_char = 'ПРОБЕЛ'
                elif c == '\n':
                    display_char = '\\n'
                else:
                    display_char = c
                f.write(f'{display_char:6} | {count:10} | {percentage:6.2f}%\n')
    except IOError as e:
        print(f"Ошибка при сохранении файла с частотами: {e}")
        raise

def apply_replacements(text, replacements):
    """
    Применяет словарь замен к тексту.
    
    Args:
        text (str): Исходный текст
        replacements (dict): Словарь замен {исходный_символ: новый_символ}
        
    Returns:
        str: Текст с примененными заменами
    """
    result = ''
    for c in text:
        if c in replacements:
            result += replacements[c]
        else:
            result += c
    return result

def save_results(decrypted_text, replacements):
    """
    Сохраняет результаты дешифровки в файлы.
    
    Args:
        decrypted_text (str): Расшифрованный текст
        replacements (dict): Словарь использованных замен
    """
    try:
        with open('decrypted.txt', 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
        
        with open('found_key.txt', 'w', encoding='utf-8') as f:
            f.write('Ключ:\n')
            for old, new in replacements.items():
                if new == ' ':
                    f.write(f'{old} -> ПРОБЕЛ\n')
                else:
                    f.write(f'{old} -> {new}\n')
    except IOError as e:
        print(f"Ошибка при сохранении файлов: {e}")

def main():
    """
    Основная функция программы.
    """
    try:
        ciphertext = load_ciphertext('cod18.txt')
    except (FileNotFoundError, UnicodeDecodeError):
        return
    
    frequencies = calculate_frequencies(ciphertext)
    display_frequencies(frequencies)
    
    try:
        save_frequencies_to_file(frequencies)
        print(f"\nФайл с частотами сохранен: frequencies.txt")
    except IOError:
        print("\nНе удалось сохранить файл с частотами")
    
    replacements = {}
    current_text = ciphertext
    
    while True:
        print('\nПолный текст сейчас:\n')
        print(current_text)
        
        print('\nТекущие замены:')
        if replacements:
            for old, new in replacements.items():
                if new == ' ':
                    print(f'  {old} -> ПРОБЕЛ')
                else:
                    print(f'  {old} -> {new}')
        else:
            print('  Замен нет')
        
        old = input('\nКакой символ заменить? (Enter - выход): ').strip().upper()
        if not old:
            break
        
        if len(old) != 1:
            print('Пожалуйста, введите один символ')
            continue
        
        new = input(f'На что заменить "{old}"? : ').strip()
        
        try:
            if new.lower() == 'пробел':
                replacements[old] = ' '
                print(f'{old} -> ПРОБЕЛ')
            else:
                replacements[old] = new.upper()
                print(f'{old} -> {new.upper()}')
            
            current_text = apply_replacements(ciphertext, replacements)
        except Exception as e:
            print(f"Ошибка при замене: {e}")
            continue
    
    if replacements:
        save_results(current_text, replacements)
        print('- decrypted.txt (расшифрованный текст)')
        print('- found_key.txt (найденный ключ)')

if __name__ == "__main__":
    main()