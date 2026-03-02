import re

class PolybiusSquare:
    """Класс для шифрования и дешифрования текста с использованием квадрата Полибия.
    
    Квадрат Полибия размером 6x6 содержит русский алфавит, пробел, цифры и знаки препинания.
    Каждый символ заменяется двузначным числом: номер строки и номер столбца.
    """
    
    def __init__(self):
        """Инициализация квадрата Полибия с русским алфавитом и дополнительными символами."""
        # Русский алфавит + пробел + цифры + знаки препинания (36 ячеек)
        self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя 0123456789.,!?-:;'
        self.size = 6
        self.square = self._create_square()
        
    def _create_square(self):
        """Создание двумерного массива 6x6 для квадрата Полибия.
        
        Returns:
            list: Двумерный список размером 6x6, содержащий символы алфавита.
        """
        square = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                idx = i * self.size + j
                row.append(self.alphabet[idx] if idx < len(self.alphabet) else '')
            square.append(row)
        return square
    
    def print_square(self):
        """Вывод квадрата Полибия в консоль в виде таблицы."""
        print("\nКвадрат Полибия:")
        print("   " + " ".join([f"{j+1:2}" for j in range(self.size)]))
        for i in range(self.size):
            row = [f"{i+1:2}"] + [f"{self.square[i][j]:2}" for j in range(self.size)]
            print(" ".join(row))
    
    def encrypt(self, text):
        """Шифрование текста с помощью квадрата Полибия.
        
        Args:
            text (str): Исходный текст для шифрования.
            
        Returns:
            str: Зашифрованный текст в виде последовательности двузначных чисел,
                 разделенных пробелами.
        """
        text = text.lower()
        # Создаем ключ: буква -> код
        key = {}
        for i in range(self.size):
            for j in range(self.size):
                if self.square[i][j]:
                    key[self.square[i][j]] = f"{i+1}{j+1}"
        
        result = []
        for char in text:
            result.append(key.get(char, char))
        return ' '.join(result)
    
    def decrypt(self, encrypted_text):
        """Дешифрование текста, зашифрованного квадратом Полибия.
        
        Args:
            encrypted_text (str): Зашифрованный текст (последовательность чисел).
            
        Returns:
            str: Расшифрованный текст.
        """
        # Создаем ключ: код -> буква
        key = {}
        for i in range(self.size):
            for j in range(self.size):
                if self.square[i][j]:
                    key[f"{i+1}{j+1}"] = self.square[i][j]
        
        # Извлекаем коды
        codes = re.sub(r'[^\d\s]', '', encrypted_text).split()
        result = []
        for code in codes:
            result.append(key.get(code, '?'))
        return ''.join(result)
    
    def save_key(self, filename):
        """Сохранение ключа шифрования в файл.
        
        Args:
            filename (str): Имя файла для сохранения ключа.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("КЛЮЧ ШИФРОВАНИЯ (буква -> код):\n")
            f.write("-"*30 + "\n")
            for i in range(self.size):
                for j in range(self.size):
                    if self.square[i][j]:
                        f.write(f"'{self.square[i][j]}' -> {i+1}{j+1}\n")

def run():
    """Запуск задания 1: шифрование текста квадратом Полибия.
    
    Функция загружает текст из файла text_for_task1.txt, шифрует его,
    сохраняет результаты и выводит на экран.
    """
    print("\n" + "="*80)
    print("ЗАДАНИЕ 1: Шифрование квадратом Полибия")
    print("="*80)
    
    # Загружаем текст из файла
    try:
        with open('text_for_task1.txt', 'r', encoding='utf-8') as f:
            original = f.read()
        print(f"Текст загружен из text_for_task1.txt (длина: {len(original)} симв.)")
    except FileNotFoundError:
        print("Ошибка: файл text_for_task1.txt не найден")
        return
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return
    
    poly = PolybiusSquare()
    poly.print_square()
    
    # Шифруем
    encrypted = poly.encrypt(original)
    print("\nЗАШИФРОВАННЫЙ ТЕКСТ:")
    print("-"*50)
    print(encrypted[:300] + "..." if len(encrypted) > 300 else encrypted)
    
    # Сохраняем
    try:
        with open('task1_encrypted.txt', 'w', encoding='utf-8') as f:
            f.write(encrypted)
        print("\n✓ Сохранено в task1_encrypted.txt")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
    
    # Ключ
    try:
        poly.save_key('task1_key.txt')
        print("✓ Ключ сохранен в task1_key.txt")
    except Exception as e:
        print(f"Ошибка при сохранении ключа: {e}")
    
    # Дешифруем
    decrypted = poly.decrypt(encrypted)
    print("\nРАСШИФРОВАННЫЙ ТЕКСТ:")
    print("-"*50)
    print(decrypted[:300] + "..." if len(decrypted) > 300 else decrypted)