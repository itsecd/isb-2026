"""
Модуль для реализации шифра Цезаря
"""


class CaesarCipher:
    """Класс для реализации шифра Цезаря"""
    
    def __init__(self, shift=3):
        """
        Инициализация шифра Цезаря
        
        Args:
            shift (int): сдвиг (ключ шифрования)
        """
        self.shift = shift
        # Русский алфавит (строчные буквы)
        self.ru_alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.ru_alphabet_upper = self.ru_alphabet_lower.upper()
        # Английский алфавит
        self.en_alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        self.en_alphabet_upper = self.en_alphabet_lower.upper()
        # Цифры
        self.digits = '0123456789'
    
    def encrypt(self, text):
        """
        Шифрование текста
        
        Args:
            text (str): исходный текст
            
        Returns:
            str: зашифрованный текст
        """
        encrypted = ''
        for char in text:
            encrypted += self._shift_char(char, self.shift)
        return encrypted
    
    def decrypt(self, text):
        """
        Расшифрование текста
        
        Args:
            text (str): зашифрованный текст
            
        Returns:
            str: расшифрованный текст
        """
        decrypted = ''
        for char in text:
            decrypted += self._shift_char(char, -self.shift)
        return decrypted
    
    def _shift_char(self, char, shift):
        """
        Сдвиг символа на заданное количество позиций
        
        Args:
            char (str): символ
            shift (int): сдвиг
            
        Returns:
            str: сдвинутый символ
        """
        # Русский алфавит
        if char in self.ru_alphabet_lower:
            idx = self.ru_alphabet_lower.index(char)
            new_idx = (idx + shift) % len(self.ru_alphabet_lower)
            return self.ru_alphabet_lower[new_idx]
        elif char in self.ru_alphabet_upper:
            idx = self.ru_alphabet_upper.index(char)
            new_idx = (idx + shift) % len(self.ru_alphabet_upper)
            return self.ru_alphabet_upper[new_idx]
        # Английский алфавит
        elif char in self.en_alphabet_lower:
            idx = self.en_alphabet_lower.index(char)
            new_idx = (idx + shift) % len(self.en_alphabet_lower)
            return self.en_alphabet_lower[new_idx]
        elif char in self.en_alphabet_upper:
            idx = self.en_alphabet_upper.index(char)
            new_idx = (idx + shift) % len(self.en_alphabet_upper)
            return self.en_alphabet_upper[new_idx]
        # Цифры
        elif char in self.digits:
            idx = self.digits.index(char)
            new_idx = (idx + shift) % len(self.digits)
            return self.digits[new_idx]
        # Остальные символы не изменяются
        else:
            return char
    
    def set_shift(self, shift):
        """
        Установка нового значения сдвига
        
        Args:
            shift (int): новое значение сдвига
        """
        self.shift = shift
    
    def get_shift(self):
        """
        Получение текущего значения сдвига
        
        Returns:
            int: текущее значение сдвига
        """
        return self.shift