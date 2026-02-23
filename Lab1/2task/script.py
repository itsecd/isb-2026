import re

def intput_file(filename: str) -> str:
    """Функция для считывания файла
    На вход принимается имя необходимого файла
    Если файл не найден будет выброшено исключение
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            print(f"File {filename} ready to work")
            return file.read()
    except FileNotFoundError:
        print("Sorry, this file impossible to detect")
        return ""

def output_file(filename: str, text: str) -> None:
    """Функция для переноса данных в необходимый файл
    На вход принимается имя файла и данные (ожидается строка)
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
        file.write("\n")
        
def parse_alfa(text: str):
    """Функция для парсинга стандартного алфавита
    с коэффициентами встречаемости
    """
    pattern = r'([А-ЯЁ=])\s*=\s*([\d.]+)'
    matches = re.findall(pattern, text)
    return {(' ' if letter == '=' else letter): float(value) for letter, value in matches}       
        
def counting_number_liter(start_string: str,total:int) -> dict:
    """Функция для подсчета частоты встречаемости букв
    в исходном тексте
    """
    freq_abs = {}
    for ch in start_string:
        freq_abs[ch] = freq_abs.get(ch, 0) + 1
    freq_percent = {ch: count / total for ch, count in freq_abs.items()}
    return freq_percent
        
def normalize_list(alfa_text: str)->dict:
    """Функция для нормализации словаря с добавлением ПРОБЕЛА
    как символа
    """
    ref_freq = parse_alfa(alfa_text)
    ref_freq[" "] = 0.128675
    if '\n' in ref_freq:
        del ref_freq['\n']
    return ref_freq

def frequency_analysis_dict(sorted_text:dict,sorted_ref:dict)-> None:
    """Функция для создания и вывода результатов сравнения
    частотного анализа
    """
    dictionary = []
    for i in range(min(len(sorted_text), len(sorted_ref))):
        text_char, text_freq = sorted_text[i]
        ref_letter, ref_freq_val = sorted_ref[i]
        dictionary.append([ref_letter, text_char])
    print("Словарь (буква -> символ):")
    print(dictionary, "\n")
    
def decrypt_with_key(key_content:dict,start_string:str)->str:
    """Функция для расшифровки текста при помощи ключа
    """
    replace_dict = {}
    for line in key_content:
        if ':' in line:
            parts = line.split(':', 1)
            src_char = parts[0].strip()
            dst_char = parts[1]       
            if src_char:
                replace_dict[src_char] = dst_char
    trans_table = str.maketrans(replace_dict)
    decrypted_text = start_string.translate(trans_table)
    return decrypted_text

def main():
    """Функция для вызова всех фунций и совокупности действия 
    """
    start_string = intput_file("text.txt")
    alfa_text = intput_file("alfa.txt")
    total = len(start_string)
    freq_percent=counting_number_liter(start_string,total)
    ref_freq=normalize_list(alfa_text)

    sorted_ref = sorted(ref_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_text = sorted(freq_percent.items(), key=lambda x: x[1], reverse=True)
    frequency_analysis_dict(sorted_text,sorted_ref)

    key_content = intput_file("key.txt").strip().splitlines()
    decrypted_text=decrypt_with_key(key_content,start_string)

    print("Результат расшифровки:")
    print(decrypted_text)
    output_file("decrypted.txt", decrypted_text)

if __name__ == "__main__":
    main()