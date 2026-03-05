import os
import sys
from typing import Dict, List, Optional, Tuple
from collections import Counter
import string


class CipherError(Exception):
    """Ошибка шифрования."""
    pass


class KeyFileError(CipherError):
    """Ошибка в файле ключа."""
    pass


class FileProcessingError(CipherError):
    """Ошибка обработки файлов."""
    pass

RUSSIAN_FREQUENCY = {
    ' ': 0.175,  # Пробел
    'О': 0.090,  # О
    'Е': 0.072,  # Е
    'А': 0.062,  # А
    'И': 0.062,  # И
    'Н': 0.053,  # Н
    'Т': 0.053,  # Т
    'С': 0.045,  # С
    'Р': 0.040,  # Р
    'В': 0.038,  # В
    'Л': 0.035,  # Л
    'К': 0.028,  # К
    'М': 0.026,  # М
    'Д': 0.025,  # Д
    'П': 0.023,  # П
    'У': 0.021,  # У
    'Я': 0.018,  # Я
    'Ы': 0.016,  # Ы
    'Ь': 0.014,  # Ь
    'Г': 0.013,  # Г
    'З': 0.012,  # З
    'Б': 0.010,  # Б
    'Ч': 0.008,  # Ч
    'Й': 0.007,  # Й
    'Х': 0.006,  # Х
    'Ж': 0.005,  # Ж
    'Ш': 0.004,  # Ш
    'Ю': 0.003,  # Ю
    'Ц': 0.003,  # Ц
    'Щ': 0.002,  # Щ
    'Э': 0.002,  # Э
    'Ф': 0.001,  # Ф
    'Ъ': 0.001,  # Ъ
}

RUSSIAN_FREQ_ORDER = [
    ' ', 'О', 'Е', 'А', 'И', 'Н', 'Т', 'С', 'Р', 'В', 'Л',
    'К', 'М', 'Д', 'П', 'У', 'Я', 'Ы', 'Ь', 'Г', 'З',
    'Б', 'Ч', 'Й', 'Х', 'Ж', 'Ш', 'Ю', 'Ц', 'Щ', 'Э', 'Ф', 'Ъ'
]


def save_frequency_analysis(input_file: str, output_file: str) -> None:
    """
    Выполняет частотный анализ файла (игнорируя символы новой строки)
    и создает файл с рекомендованным ключом на основе частотного анализа.

    Args:
        input_file: Путь к входному файлу с текстом.
        output_file: Путь к файлу для сохранения результатов анализа.

    Raises:
        FileProcessingError: При ошибках чтения/записи файлов.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except (FileNotFoundError, IOError) as e:
        raise FileProcessingError(f"Ошибка чтения файла '{input_file}': {e}") from e

    if not text:
        raise FileProcessingError("Файл пуст")

    original_length = len(text)
    text_without_newlines = text.replace('\n', '').replace('\r', '')
    newlines_count = original_length - len(text_without_newlines)
    
    counter = Counter(text_without_newlines)
    total_chars = len(text_without_newlines)
    
    text_freq = counter.most_common()
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("РЕКОМЕНДОВАННЫЙ КЛЮЧ\n")
            f.write("(на основе частотного анализа)\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Исходный файл: {input_file}\n")
            f.write(f"Всего символов в файле (с \\n): {original_length}\n")
            f.write(f"Символов новой строки удалено из анализа: {newlines_count}\n")
            f.write(f"Символов для анализа (без \\n): {total_chars}\n\n")
            
            f.write("Самые частые символы в тексте (слева) должны соответствовать\n")
            f.write("самым частым символам русского языка (справа):\n\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"{'№':<4} {'Символ в тексте':<20} {'Частота %':<12} {'→ Русский символ':<20} {'Частота %'}\n")
            f.write("-" * 80 + "\n")
            
            max_items = min(len(text_freq), len(RUSSIAN_FREQ_ORDER))
            
            for i in range(max_items):
                text_char, text_count = text_freq[i]
                text_percent = (text_count / total_chars) * 100
                
                russian_char = RUSSIAN_FREQ_ORDER[i]
                russian_percent = RUSSIAN_FREQUENCY[russian_char] * 100
                
                text_display = f"'{text_char}'" if text_char != ' ' else "' ' (ПРОБЕЛ)"
                russian_display = russian_char if russian_char != ' ' else 'ПРОБЕЛ'
                
                f.write(f"{i+1:<4} {text_display:<20} {text_percent:>6.2f}%      → {russian_display:<20} {russian_percent:>6.2f}%\n")
            
            if len(text_freq) > len(RUSSIAN_FREQ_ORDER):
                f.write("\n" + "-" * 80 + "\n")
                f.write("Дополнительные символы в тексте (меньшей частоты):\n")
                f.write("-" * 80 + "\n")
                
                for i in range(len(RUSSIAN_FREQ_ORDER), len(text_freq)):
                    text_char, text_count = text_freq[i]
                    text_percent = (text_count / total_chars) * 100
                    text_display = f"'{text_char}'" if text_char != ' ' else "' ' (ПРОБЕЛ)"
                    f.write(f"{i+1:<4} {text_display:<20} {text_percent:>6.2f}%      → (нет соответствия)\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:\n")
            f.write("=" * 80 + "\n")
            f.write("1. Откройте программу и выберите пункт 2 'Создать ключ'\n")
            f.write("2. В интерактивном режиме добавляйте замены по одной:\n")
            f.write("   - Для символов из левой колонки указывайте соответствующие\n")
            f.write("     русские символы из правой колонки\n")
            f.write("3. Формат ввода: символ_шифротекста=символ_расшифровки\n")
            f.write("   Например: если символ 'X' должен стать 'О', введите: X=О\n")
            f.write("4. Для пробела используйте ' ' или слово 'ПРОБЕЛ'\n")
            f.write("5. После добавления всех замен сохраните ключ в файл\n\n")
            
            f.write("ПРИМЕЧАНИЕ: Символы новой строки (\\n) были исключены из анализа\n")
            f.write("и при создании ключа их можно игнорировать.\n")
            
    except IOError as e:
        raise FileProcessingError(f"Ошибка записи в файл '{output_file}': {e}") from e
    
    print(f"\nФайл с рекомендованным ключом сохранен: {output_file}")
    print(f"Всего символов в файле (с \\n): {original_length}")
    print(f"Символов новой строки удалено из анализа: {newlines_count}")
    print(f"Символов для анализа (без \\n): {total_chars}")
    print(f"Уникальных символов: {len(counter)}")
    print(f"\nВ файле представлено {min(len(text_freq), len(RUSSIAN_FREQ_ORDER))} рекомендованных соответствий.")


def interactive_key_creation(encrypted_text: str) -> Tuple[Dict[str, str], bool]:
    """
    Интерактивное создание ключа с пошаговым добавлением замен.

    Args:
        encrypted_text: Зашифрованный текст.

    Returns:
        Кортеж (созданный ключ, флаг завершения).
    """
    current_key = {}    
    
    print("\n" + "=" * 70)
    print("СОЗДАНИЕ КЛЮЧА")
    print("=" * 70)
    print("Добавляйте замены по одной в формате: символ_шифротекста=символ_расшифровки")
    print("Для пробела используйте ' ' или напишите 'ПРОБЕЛ'")
    print("Для завершения и сохранения ключа введите 'ГОТОВО'")
    print("-" * 70)
    
    while True:
        print("\n" + "=" * 70)
        print("ТЕКУЩИЙ РЕЗУЛЬТАТ РАСШИФРОВКИ (первые 500 символов):")
        print("-" * 70)
        
        if current_key:
            decrypted = decrypt_text(encrypted_text, current_key)
            print(decrypted[:500])
            if len(decrypted) > 500:
                print("...")
        else:
            print("(ключ пуст - отображается исходный текст)")
            print(encrypted_text[:500])
            if len(encrypted_text) > 500:
                print("...")
        
        print("\n" + "-" * 70)
        print(f"ТЕКУЩИЙ КЛЮЧ ({len(current_key)} замен):")
        if current_key:
            for from_char, to_char in sorted(current_key.items()):
                from_display = from_char if from_char != ' ' else 'ПРОБЕЛ'
                to_display = to_char if to_char != ' ' else 'ПРОБЕЛ'
                print(f"  '{from_display}' -> '{to_display}'")
        else:
            print("  (ключ пуст)")
        
        print("\nДЕЙСТВИЯ:")
        print("1. Добавить замену")
        print("2. Удалить замену")
        print("3. Сбросить все замены")
        print("4. Закончить создание ключа и сохранить")
        
        action = input("\nВыберите действие (1-4): ").strip()
        
        if action == '1':
            substitution = input("Введите замену в формате 'символ_шифротекста=символ_расшифровки': ").strip()
            
            if substitution.upper() == 'ГОТОВО':
                return current_key, True
            
            if substitution[1]=='=':
                from_char = substitution[0]
                to_char = substitution[2] 

                if from_char and to_char:
                    if from_char.upper() in ('пробел', 'ПРОБЕЛ'):
                        from_char = ' '
                    else:
                        from_char = from_char[0]
                    
                    if to_char.upper() in ('пробел', 'ПРОБЕЛ'):
                        to_char = ' '
                    else:
                        to_char = to_char[0]
                    
                    if to_char in current_key.values():
                        print(f"Предупреждение: символ '{to_char}' уже используется в ключе!")
                        confirm = input("Продолжить? (д/н): ").strip().lower()
                        if confirm not in ('д', 'да', 'y', 'yes'):
                            continue
                    
                    current_key[from_char] = to_char
                    print(f"Добавлена замена: '{from_char}' -> '{to_char}'")
                    
                    print("\nОБНОВЛЕННЫЙ РЕЗУЛЬТАТ (первые 300 символов):")
                    new_decrypted = decrypt_text(encrypted_text, current_key)
                    display_text = new_decrypted.replace('\n', '¶\n')
                    print(display_text[:300])
                else:
                    print("Ошибка: неверный формат")
            else:
                print("Ошибка: отсутствует символ '='")
                
        elif action == '2':
            if not current_key:
                print("Ключ пуст, нечего удалять")
                continue
                
            from_char = input("Введите символ шифротекста для удаления из ключа: ").strip()
            if from_char:
                if from_char.upper() in ('ПРОБЕЛ', 'ПРОБЕЛ'):
                    from_char = ' '
                else:
                    from_char = from_char[0]
                    
                if from_char in current_key:
                    del current_key[from_char]
                    print(f"Удалена замена для символа '{from_char}'")
                else:
                    print(f"Символ '{from_char}' не найден в ключе")
                    
        elif action == '3':
            confirm = input("Сбросить все замены? (д/н): ").strip().lower()
            if confirm in ('д', 'да', 'y', 'yes'):
                current_key.clear()
                print("Ключ сброшен")
                
        elif action == '4':
            return current_key, True
        else:
            print("Неверный выбор. Пожалуйста, выберите 1-4.")


def save_key_to_txt(key_map: Dict[str, str], key_file: str) -> None:
    """
    Сохраняет ключ шифрования в текстовый файл.

    Args:
        key_map: Словарь с парами замены.
        key_file: Путь к файлу для сохранения.
    """
    try:
        with open(key_file, 'w', encoding='utf-8') as f:
            f.write("# Ключ\n")
            f.write("# Формат: символ_шифротекста=символ_расшифровки\n")
            f.write("# Для пробела используется символ пробела\n\n")
            
            for original, replacement in sorted(key_map.items()):
                f.write(f"{replacement}={original}\n")
        
        print(f"\nКлюч успешно сохранен в файл: {key_file}")
        print(f"Всего сохранено замен: {len(key_map)}")
    except IOError as e:
        print(f"Ошибка сохранения ключа: {e}")


def decrypt_text(text: str, key_map: Dict[str, str]) -> str:
    """
    Дешифрует текст, используя обратную замену.

    Args:
        text: Зашифрованный текст.
        key_map: Словарь с парами замены.

    Returns:
        Расшифрованный текст.
    """
    result_chars = []
    for char in text:
        if char in key_map:
            result_chars.append(key_map[char])
        else:
            result_chars.append(char)
    return ''.join(result_chars)


def load_text_from_file(file_path: str) -> str:
    """
    Загружает текст из файла.

    Args:
        file_path: Путь к файлу.

    Returns:
        Содержимое файла.

    Raises:
        FileProcessingError: При ошибке чтения файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError) as e:
        raise FileProcessingError(f"Ошибка чтения файла '{file_path}': {e}") from e


def get_user_choice() -> str:
    """
    Получает выбор пользователя из меню.

    Returns:
        Выбранный пункт меню.
    """
    while True:
        print("\n" + "=" * 70)
        print("ПРОГРАММА ДЛЯ РАБОТЫ С ШИФРОМ ПРОСТОЙ ЗАМЕНЫ")
        print("=" * 70)
        print("1. Создать файл с рекомендованным ключом (частотный анализ)")
        print("2. Создать ключ (интерактивный режим)")
        print("3. Выход")

        choice = input("\nВыберите действие (1-3): ").strip()

        if choice in ('1', '2', '3'):
            return choice

        print("Неверный выбор. Пожалуйста, выберите 1-3.")


def main() -> None:
    """Основная функция программы."""
    while True:
        try:
            choice = get_user_choice()

            if choice == '1': 
                print("\n--- СОЗДАНИЕ ФАЙЛА С РЕКОМЕНДОВАННЫМ КЛЮЧОМ ---")
                
                input_file = input("Введите путь к TXT файлу с шифротекстом: ").strip()
                if not os.path.exists(input_file):
                    print(f"Ошибка: файл '{input_file}' не найден")
                    continue
                
                output_file = input("Введите путь для сохранения файла с рекомендациями: ").strip()
                if not output_file.lower().endswith('.txt'):
                    output_file += '.txt'
                
                save_frequency_analysis(input_file, output_file)

            elif choice == '2':  
                print("\n--- СОЗДАНИЕ КЛЮЧА ---")
                
                input_file = input("Введите путь к TXT файлу с шифротекстом: ").strip()
                if not os.path.exists(input_file):
                    print(f"Ошибка: файл '{input_file}' не найден")
                    continue
                
                encrypted_text = load_text_from_file(input_file)
                print(f"\nЗагружен текст из файла: {len(encrypted_text)} символов (включая \\n)")
                
                newlines_count = encrypted_text.count('\n')
                print(f"Символов новой строки в тексте: {newlines_count}")
                print(f"Первые 100 символов (¶ обозначает символ новой строки):")
                display_text = encrypted_text[:100].replace('\n', '¶\n')
                print(display_text)
                
                key_map, completed = interactive_key_creation(encrypted_text)
                
                if completed and key_map:
                    key_file = input("\nВведите имя файла для сохранения ключа: ").strip()
                    if not key_file.lower().endswith('.txt'):
                        key_file += '.txt'
                    
                    save_key_to_txt(key_map, key_file)
                    
                    print("\n" + "=" * 70)
                    print("ИТОГОВЫЙ РЕЗУЛЬТАТ РАСШИФРОВКИ:")
                    print("=" * 70)
                    decrypted = decrypt_text(encrypted_text, key_map)
                    display_text = decrypted[:1000].replace('\n', '¶\n')
                    print(display_text)
                    if len(decrypted) > 1000:
                        print("...")
                        
                elif not key_map:
                    print("\nКлюч не был создан.")
                else:
                    print("\nСоздание ключа прервано.")

            elif choice == '3': 
                print("\nДо свидания!")
                break

        except FileProcessingError as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()