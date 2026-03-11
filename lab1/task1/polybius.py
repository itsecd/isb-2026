# -*- coding: utf-8 -*-
# polybius.py

import os

class PolybiusSquare:
    """Шифрование заменой букв на координаты в таблице 6x6."""
    
    def __init__(self, square_file="square.txt"):
        """Инициализация квадрата из файла или создание стандартного."""
        self.square = []
        self.pos = {}
        
        for i in range(6):
            row = ['.'] * 6
            self.square.append(row)
        
        if not os.path.exists(square_file):
            self._create_default_square()
        else:
            self._load_from_file(square_file)
        
        self._build_position_map()
    
    def _load_from_file(self, filename):
        """Загрузка квадрата из файла формата 'строка,столбец:символ'."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    for part in parts:
                        if ':' not in part:
                            continue
                        
                        coord_part, letter = part.split(':')
                        if ',' not in coord_part:
                            continue
                        
                        row_str, col_str = coord_part.split(',')
                        row = int(row_str) - 1
                        col = int(col_str) - 1
                        
                        if 0 <= row < 6 and 0 <= col < 6:
                            self.square[row][col] = letter
        except:
            self._create_default_square()
    
    def _create_default_square(self):
        """Стандартный квадрат с русским алфавитом и знаками препинания."""
        self.square = [
            ['А', 'Б', 'В', 'Г', 'Д', 'Е'],
            ['Ё', 'Ж', 'З', 'И', 'Й', 'К'],
            ['Л', 'М', 'Н', 'О', 'П', 'Р'],
            ['С', 'Т', 'У', 'Ф', 'Х', 'Ц'],
            ['Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь'],
            ['Э', 'Ю', 'Я', '-', '.', ',']
        ]
    
    def _build_position_map(self):
        """Создание словаря {символ: (строка, столбец)}."""
        self.pos = {}
        for i in range(6):
            for j in range(6):
                letter = self.square[i][j]
                if letter and letter != '.':
                    self.pos[letter] = (i + 1, j + 1)
    
    def encrypt(self, text):
        """
        Шифрование текста.
        
        Возвращает строку с координатами букв через пробел.
        Пробелы сохраняются.
        """
        result = []
        for char in text:
            upper_char = char.upper()
            
            if upper_char == ' ':
                result.append('')
            elif upper_char in self.pos:
                row, col = self.pos[upper_char]
                result.append(f"{row}{col}")
            else:
                result.append(char)
        
        return ' '.join(result)
    
    def decrypt(self, encrypted_text):
        """
        Дешифрование текста.
        
        Неизвестные символы заменяются на '?'.
        """
        parts = encrypted_text.split(' ')
        result = []
        
        for part in parts:
            if part == '':
                result.append(' ')
            elif len(part) == 2 and part.isdigit():
                row = int(part[0]) - 1
                col = int(part[1]) - 1
                
                if 0 <= row < 6 and 0 <= col < 6:
                    letter = self.square[row][col]
                    result.append(letter if letter != '.' else '?')
                else:
                    result.append('?')
            else:
                result.append(part)
        
        return ''.join(result)
    
    def show(self):
        """Вывод квадрата в консоль."""
        print("\n Квадрат Полибия:")
        print("   " + "  ".join([str(i+1) for i in range(6)]))
        for i, row in enumerate(self.square):
            print(f"{i+1}  " + "  ".join(row))
        print()
