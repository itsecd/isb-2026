import os

def caesar_cipher(text, shift):
    result = ""
    
    for char in text:
        if char.isalpha():
            if char.isupper():
                # Для заглавных букв (american версия)
                if 'A' <= char <= 'Z':
                    shifted = (ord(char) - 65 + shift) % 26 + 65
                else:
                    # Для кириллицы (Наш )
                    shifted = (ord(char) - 1040 + shift) % 32 + 1040
                result += chr(shifted)
            else:
                # Для строчных букв
                if 'a' <= char <= 'z':
                    shifted = (ord(char) - 97 + shift) % 26 + 97
                else:
                    # Для кириллицы
                    shifted = (ord(char) - 1072 + shift) % 32 + 1072
                result += chr(shifted)
        else:
            result += char
    
    return result

def read_from_file(filename):
    """Читаем текст из файла с проверкой на пустоту"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Проверка на пустой файл
            if not content:
                print(f"Внимание: Файл '{filename}' пустой!")
                return "empty"
            
            # Проверка на файл только с пробелами и спецсимволами
            if not any(c.isalpha() for c in content):
                print(f"Внимание: В файле '{filename}' нет букв для шифрования!")
                return "no_letters"
            
            return content
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def write_to_file(filename, text):
    """Записываем текст в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Текст успешно записан в файл '{filename}'")
        return True
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
        return False

def get_non_empty_filename(prompt, check_exists=True):
    """Запрашиваем имя файла и проверяем, что оно не пустое"""
    while True:
        filename = input(prompt).strip()
        if not filename:
            print("Имя файла не может быть пустым!")
            continue
        
        if check_exists and not os.path.exists(filename):
            print(f"Файл '{filename}' не существует!")
            continue
            
        return filename
def main():
    print("Шифр Цезаря (выбор файла)\n")
    
    while True:
        print("Выберите действие:")
        print("  1. Указать имя файла для шифрования")
        print("  2. Выход")
        
        choice = input("\nВаш выбор (1/2): ").strip()
        '''Начал с самого простого)'''
        if choice == '2':
            print("Выход....")
            return
        
        elif choice == '1':
            # Выбор исходного файла с проверкой на пустое имя
            input_file = get_non_empty_filename("\nВведите имя файла с исходным текстом: ")
            
            # Читаем исходный текст из файла с проверкой на пустоту
            print(f"Читаем текст из файла '{input_file}'...")
            text = read_from_file(input_file)
            
            if text is None:
                continue
            # Обработка специальных случаев
            if text == "empty":
                print("Невозможно зашифровать пустой файл. Добавьте текст в файл и попробуйте снова.")
                continue
            elif text == "no_letters":
                print("Невозможно зашифровать файл без букв. Добавьте текст с буквами и попробуйте снова.")
                continue
            print(f"\nИсходный текст ({len(text)} символов, {sum(c.isalpha() for c in text)} букв):")
            print("-" * 50)
            # Показываем первые 100 символов чтобы убедиться что наш текст и всё тип-топ
            preview = text[:100] + "..." if len(text) > 100 else text
            print(preview)
            print("-" * 50)
            # Ввод сдвига (ключа)
            while True:
                try:
                    shift = int(input("\nВведите ключ (сдвиг, целое число): "))# и тут проверка на дурачка
                    break
                except ValueError:
                    print("Ошибка! Введите целое число.")
            # Шифрование
            encrypted_text = caesar_cipher(text, shift)
            
            # Выбор файла для сохранения результата
            output_file = input("\nВведите имя файла для сохранения результата (Enter для 'encrypted.txt'): ").strip()
            if not output_file:
                output_file = "encrypted.txt"
            
            # Сохраняем зашифрованный текст в файл
            if write_to_file(output_file, encrypted_text):
                print(f"\nШифрование завершено!")
                print(f"   Исходный файл: '{input_file}' ({len(text)} символов)")
                print(f"   Зашифрованный файл: '{output_file}' ({len(encrypted_text)} символов)")
                print(f"   Ключ (сдвиг): {shift}")
                
                # Для проверки: расшифровка c обратным значением
                print("\nПроверка расшифровки (используем тот же ключик со знаком минус):")
                decrypted_text = caesar_cipher(encrypted_text, -shift)
                preview_dec = decrypted_text[:100] + "..." if len(decrypted_text) > 100 else decrypted_text
                print(preview_dec)  
            print("\n" + "="*50 + "\n")    
        else:
            print("НЕПРАУИЛЬНЫЙ ВЫБОР!!!. Выберите 1 или 2.")
if __name__ == "__main__":
    main()