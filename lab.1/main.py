"""
Лабораторная работа: Шифр простой подстановки (моноалфавитная замена)
"""

import random
import os

def read_text_from_file():
    """Читает текст из txt файла """
    while True:
        # Показываем доступные txt файлы
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f not in ['encrypted.txt', 'my_key.txt']]
        
        print("\nДОСТУПНЫЕ ТЕКСТОВЫЕ ФАЙЛЫ:")
        if not txt_files:
            print("  Нет доступных .txt файлов (кроме encrypted.txt и my_key.txt)")
            filename = input("Введите имя файла вручную (или 'exit' для выхода): ").strip()
            if filename.lower() == 'exit':
                print("Программа завершена.")
                exit()
        else:
            for i, file in enumerate(txt_files, 1):
                # Показываем размер файла
                size = os.path.getsize(file)
                print(f"  {i} - {file} ({size} байт)")
            print("  0 - Ввести имя вручную")
            print("  q - Выход")
            
            choice = input("\nВыберите файл (номер, имя или 0): ").strip()
            
            if choice.lower() == 'q':
                print("Программа завершена.")
                exit()
            
            # Проверяем, является ли выбор числом (номером из списка)
            if choice.isdigit():
                choice_num = int(choice)
                if choice_num == 0:
                    filename = input("Введите имя файла вручную: ").strip()
                elif 1 <= choice_num <= len(txt_files):
                    filename = txt_files[choice_num - 1]
                else:
                    print(f"✗ Неверный номер. Введите число от 0 до {len(txt_files)}")
                    continue
            else:
                # Пользователь ввёл имя файла напрямую
                filename = choice
        
        # Пробуем прочитать файл
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) == 0:
                    print(f"✗ Файл '{filename}' пуст!")
                    continue
                print(f"✓ Файл '{filename}' успешно загружен")
                print(f"  • Размер: {len(content)} символов")
                print(f"  • Первые 50 символов: {repr(content[:50])}...")
                return content
        except FileNotFoundError:
            print(f"✗ Файл '{filename}' не найден!")
        except UnicodeDecodeError:
            print(f"✗ Файл '{filename}' имеет неправильную кодировку. Используйте UTF-8.")
        except Exception as e:
            print(f"✗ Ошибка при чтении файла: {e}")


class Cipher:
    """Простой шифр замены"""
    
    def __init__(self):
        self.encrypt_dict = {}  # словарь для шифрования
        self.decrypt_dict = {}  # словарь для расшифровки
    
    def generate_key(self, text):
        """Создает случайный ключ на основе текста"""
        # Все уникальные символы в тексте
        chars = sorted(list(set(text)))
        
        # Перемешиваем их
        shuffled = chars.copy()
        random.shuffle(shuffled)
        
        # Создаем словари
        self.encrypt_dict = {chars[i]: shuffled[i] for i in range(len(chars))}
        self.decrypt_dict = {shuffled[i]: chars[i] for i in range(len(chars))}
        
        return self.encrypt_dict
    
    def set_key(self, key_dict):
        """Устанавливает свой ключ"""
        self.encrypt_dict = key_dict
        self.decrypt_dict = {v: k for k, v in key_dict.items()}
    
    def encrypt(self, text):
        """Шифрует текст"""
        result = ''
        for char in text:
            result += self.encrypt_dict.get(char, char)
        return result
    
    def decrypt(self, text):
        """Расшифровывает текст"""
        result = ''
        for char in text:
            result += self.decrypt_dict.get(char, char)
        return result
    
    def save_key(self, filename):
        """Сохраняет ключ в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# КЛЮЧ ШИФРОВАНИЯ\n")
            f.write("# Формат: исходный_символ -> зашифрованный_символ\n\n")
            for orig, enc in sorted(self.encrypt_dict.items()):
                # Для специальных символов
                o = 'ПРОБЕЛ' if orig == ' ' else orig
                e = 'ПРОБЕЛ' if enc == ' ' else enc
                f.write(f"{o} -> {e}\n")
        print(f"✓ Ключ сохранен в {filename}")
    
    def load_key(self, filename):
        """Загружает ключ из файла"""
        try:
            key_dict = {}
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '->' in line and not line.startswith('#'):
                        parts = line.split('->')
                        if len(parts) == 2:
                            o = parts[0].strip()
                            e = parts[1].strip()
                            # Восстанавливаем пробелы
                            if o == 'ПРОБЕЛ':
                                o = ' '
                            if e == 'ПРОБЕЛ':
                                e = ' '
                            key_dict[o] = e
            self.set_key(key_dict)
            print(f"✓ Ключ загружен из {filename}")
            return True
        except Exception as e:
            print(f"✗ Ошибка загрузки ключа: {e}")
            return False
    
    def show_key_sample(self, n=15):
        """Показывает пример ключа"""
        items = list(self.encrypt_dict.items())[:n]
        print("\nТЕКУЩИЙ КЛЮЧ (первые 15 замен):")
        print("-" * 30)
        for orig, enc in items:
            o = '⎵' if orig == ' ' else orig
            e = '⎵' if enc == ' ' else enc
            print(f"  '{o}' -> '{e}'")
        print(f"  ... и еще {len(self.encrypt_dict) - n} замен")
    
    def edit_mapping(self):
        """Ручное редактирование одной замены"""
        print("\nДОСТУПНЫЕ СИМВОЛЫ ДЛЯ ЗАМЕНЫ:")
        # Показываем все символы
        chars = list(self.encrypt_dict.keys())
        chars_display = []
        for c in chars[:20]:  # покажем первые 20
            chars_display.append('⎵' if c == ' ' else c)
        print(' '.join(chars_display))
        if len(chars) > 20:
            print(f"... и еще {len(chars) - 20} символов")
        
        orig = input("\nВведите символ, который хотите заменить: ")
        if orig in self.encrypt_dict:
            current = self.encrypt_dict[orig]
            cur_disp = '⎵' if current == ' ' else current
            print(f"Сейчас заменяется на: '{cur_disp}'")
            
            new = input("Введите новый символ для замены: ")
            
            # Проверка уникальности
            if new in self.decrypt_dict and self.decrypt_dict[new] != orig:
                new_disp = '⎵' if new == ' ' else new
                old_orig = self.decrypt_dict[new]
                old_disp = '⎵' if old_orig == ' ' else old_orig
                print(f"✗ Ошибка: символ '{new_disp}' уже используется для '{old_disp}'")
            else:
                # Удаляем старую связь
                old = self.encrypt_dict[orig]
                del self.decrypt_dict[old]
                # Создаем новую
                self.encrypt_dict[orig] = new
                self.decrypt_dict[new] = orig
                print("✓ Замена обновлена")
        else:
            print("✗ Символ не найден")


def main():
    """Главная функция"""
    print("=" * 60)
    print("ШИФР ПРОСТОЙ ПОДСТАНОВКИ (МОНОАЛФАВИТНАЯ ЗАМЕНА)")
    print("=" * 60)
    
    # Создаем шифр
    cipher = Cipher()
    
    # Читаем текст из выбранного файла
    TEXT = read_text_from_file()
    
    # Показываем информацию о тексте
    print(f"\nИСХОДНЫЙ ТЕКСТ:")
    print(f"  • Полная длина: {len(TEXT)} символов")
    print(f"  • Уникальных символов: {len(set(TEXT))}")
    
    # Генерируем ключ
    cipher.generate_key(TEXT)
    cipher.show_key_sample()
    
    # Сразу шифруем текст
    encrypted = cipher.encrypt(TEXT)
    with open('encrypted.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted)
    print("\n✓ Текст зашифрован и сохранен в encrypted.txt")
    
    # Проверяем расшифровку
    decrypted = cipher.decrypt(encrypted)
    if decrypted == TEXT:
        print("✓ Проверка пройдена: расшифровка работает правильно")
    else:
        print("✗ Ошибка: расшифровка не работает!")
    
    # Меню (только действия с ключом)
    while True:
        print("\n" + "=" * 40)
        print("ДЕЙСТВИЯ С КЛЮЧОМ:")
        print("1 - Показать текущий ключ")
        print("2 - Сохранить ключ в файл")
        print("3 - Загрузить ключ из файла")
        print("4 - Сгенерировать новый ключ")
        print("5 - Изменить одну замену вручную")
        print("0 - Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == '1':
            cipher.show_key_sample(20)
            
        elif choice == '2':
            cipher.save_key('my_key.txt')
            
        elif choice == '3':
            cipher.load_key('my_key.txt')
            # Перешифровываем текст с новым ключом
            encrypted = cipher.encrypt(TEXT)
            with open('encrypted.txt', 'w', encoding='utf-8') as f:
                f.write(encrypted)
            print("✓ Текст перешифрован с новым ключом")
            
        elif choice == '4':
            cipher.generate_key(TEXT)
            cipher.show_key_sample()
            # Перешифровываем текст
            encrypted = cipher.encrypt(TEXT)
            with open('encrypted.txt', 'w', encoding='utf-8') as f:
                f.write(encrypted)
            print("✓ Сгенерирован новый ключ, текст перешифрован")
            
        elif choice == '5':
            cipher.edit_mapping()
            # Перешифровываем текст после изменения
            encrypted = cipher.encrypt(TEXT)
            with open('encrypted.txt', 'w', encoding='utf-8') as f:
                f.write(encrypted)
            print("✓ Текст перешифрован с измененным ключом")
            
        elif choice == '0':
            print("\nПрограмма завершена")
            print(f"Зашифрованный текст сохранен в encrypted.txt")
            print(f"Ключ сохранен в my_key.txt (если вы его сохраняли)")
            break


if __name__ == "__main__":
    main()