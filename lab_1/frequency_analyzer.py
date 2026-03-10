"""
Модуль для частотного анализа текста
"""


class FrequencyAnalyzer:
    """Класс для частотного анализа текста"""
    
    def __init__(self):
        # Частоты букв в русском языке (приблизительные)
        self.ru_freq = {
            'о': 0.1118, 'а': 0.0802, 'е': 0.0768, 'и': 0.0709,
            'н': 0.0653, 'т': 0.0626, 'с': 0.0547, 'р': 0.0534,
            'в': 0.0457, 'л': 0.0421, 'к': 0.0349, 'м': 0.0321,
            'д': 0.0298, 'п': 0.0279, 'у': 0.0261, 'я': 0.0201,
            'ы': 0.0189, 'з': 0.0166, 'ь': 0.0162, 'г': 0.0160,
            'ч': 0.0144, 'й': 0.0121, 'х': 0.0097, 'ж': 0.0094,
            'б': 0.0089, 'ю': 0.0064, 'ш': 0.0064, 'э': 0.0032,
            'щ': 0.0030, 'ф': 0.0026, 'ъ': 0.0014, 'ё': 0.0001
        }
        
        # Частоты букв в английском языке
        self.en_freq = {
            'e': 0.1270, 't': 0.0906, 'a': 0.0817, 'o': 0.0751,
            'i': 0.0697, 'n': 0.0675, 's': 0.0633, 'h': 0.0609,
            'r': 0.0599, 'd': 0.0425, 'l': 0.0403, 'c': 0.0278,
            'u': 0.0276, 'm': 0.0241, 'w': 0.0236, 'f': 0.0223,
            'g': 0.0202, 'y': 0.0197, 'p': 0.0193, 'b': 0.0149,
            'v': 0.0098, 'k': 0.0077, 'j': 0.0015, 'x': 0.0015,
            'q': 0.0010, 'z': 0.0007
        }
    
    def analyze(self, text):
        """
        Анализ частоты символов в тексте
        
        Args:
            text (str): текст для анализа
            
        Returns:
            dict: словарь с частотами символов (отсортированный по убыванию)
        """
        freq = {}
        total_chars = 0
        
        for char in text.lower():
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1
                total_chars += 1
        
        # Преобразуем в проценты
        for char in freq:
            freq[char] = round(freq[char] / total_chars * 100, 2) if total_chars > 0 else 0
        
        # Сортируем по убыванию частоты
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_freq)
    
    def print_frequency_table(self, freq_dict):
        """
        Вывод таблицы частот в консоль
        
        Args:
            freq_dict (dict): словарь с частотами
        """
        print("\n" + "="*40)
        print("ТАБЛИЦА ЧАСТОТ СИМВОЛОВ")
        print("="*40)
        print(f"{'Символ':<10} {'Частота (%)':<15}")
        print("-"*40)
        for char, freq in freq_dict.items():
            print(f"{char:<10} {freq:<15.2f}")
        print("="*40)
    
    def save_frequency_table(self, freq_dict, filename):
        """
        Сохранение таблицы частот в файл
        
        Args:
            freq_dict (dict): словарь с частотами
            filename (str): имя файла для сохранения
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ТАБЛИЦА ЧАСТОТ СИМВОЛОВ\n")
            f.write("="*40 + "\n")
            f.write(f"{'Символ':<10} {'Частота (%)':<15}\n")
            f.write("-"*40 + "\n")
            for char, freq in freq_dict.items():
                f.write(f"{char:<10} {freq:<15.2f}\n")
            f.write("="*40 + "\n")
    
    def get_most_common_chars(self, freq_dict, count=5):
        """
        Получение наиболее частых символов
        
        Args:
            freq_dict (dict): словарь с частотами
            count (int): количество символов для возврата
            
        Returns:
            list: список наиболее частых символов
        """
        return list(freq_dict.keys())[:count]