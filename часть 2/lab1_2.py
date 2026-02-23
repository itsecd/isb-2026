def read_file(file_path: str) -> str:
    """
    Читает файл и возвращает содержимое одной строкой.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print(f"Файл {file_path} успешно загружен")
            return file.read()
    except FileNotFoundError:
        print("Ошибка: файл не найден")
        return ""
    
def write_file(file_path: str, text: str) -> None:
    """
    Записывает текст в файл.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def count(data: str) -> dict:
    """
    Подсчёт количества символов в изначальном тексте
    """
    counts={}
    for symb in data:
        if symb in counts:
            counts[symb] += 1
        else:
            counts[symb]=1
    return counts

def freq_t(count: dict, total: int) -> dict:
    """
    Переработка в частоту появления букв в файле
    """
    freq={}
    for symb, cnt in count.items():
        freq[symb] = cnt/total
    return freq

def parse(text: str) -> dict:
    """
    Парсинг по знаку = и возвращение словаря
    """
    result = {}
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or '=' not in line:
            continue
            
        parts = line.split('=', 1)
        left = parts[0].strip()
        right = float(parts[1].strip())
        
        if left == '':
            result[' '] = right
        else:
            result[left] = right
    
    return result

def final_produce(key_text: dict,orig_string: str)->str:
    """
    Перевод при помощи maketrans с использованнием ключа из файла
    """
    trans_map = {}
    for entry in key_text:
        if '=' in entry:
            left_part, right_part = entry.split('=', 1)
            key_char = left_part.strip()
            value_char = right_part.strip()
            if key_char:
                trans_map[key_char] = value_char
    trans_map[">"] = " "
    trans_map[" "] = "Я"
    conversion_table = str.maketrans(trans_map)
    decoded_result = orig_string.translate(conversion_table)
    return decoded_result

def main():
    orig_string = read_file("orig.txt")
    freq_et = read_file("freq.txt")
    
    if not orig_string or not freq_et:
        return
    
    total = len(orig_string)
    etalon_freq = parse(freq_et)
    counts = count(orig_string)
    text_freq = freq_t(counts, total)
    
    sorted_etalon = sorted(etalon_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_text = sorted(text_freq.items(), key=lambda x: x[1], reverse=True)
    
    key_dict = {}
    length = min(len(sorted_text), len(sorted_etalon))
    for i in range(length):
        text_symbol = sorted_text[i][0]
        etalon_letter = sorted_etalon[i][0]
        key_dict[text_symbol] = etalon_letter
    print(key_dict)
    key_text = read_file("key.txt").strip().split('\n')
    decoded_result=final_produce(key_text,orig_string)
    print("\nРезультат расшифровки:")
    print(decoded_result)
    
    write_file("decrypted.txt", decoded_result)
    print("Результат сохранен в decrypted.txt")

if __name__ == "__main__":
    main()