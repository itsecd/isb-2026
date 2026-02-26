import sys
import argparse

def intput_file(filename: str) -> str:
    """Функция для считывания файла
    На вход принимается имя необходимого файла
    Если файл не найден будет выброшено исключение
    """
    try:
        file = open(filename, "r", encoding="utf-8")
        print(f"File {filename} ready to work")
        text = file.read()
        file.close()
        return text
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

def normalize_str(start_string: str) -> str:
    """Функция для нормализации строки перед шифрованием
    на вход принимает считанную раннее строку текста
    """
    produce_string = ""
    for liter in start_string:
        if liter.isalpha():
           produce_string += liter.upper()
    return produce_string

def code_produce(produce_string: str, polybius_square: list) -> list:
    """Функция для конвертации букв исходного текста в пары чисел
    для последующего шифрования
    """
    number_vector = []
    for liter in produce_string:
        found = False
        for i in range(5):
            for j in range(5):
                cell = polybius_square[i][j]
                if cell == 'I/J':
                    if liter in ('I', 'J'):
                        number_vector.append([i, j])
                        found = True
                        break
                elif liter == cell:
                    number_vector.append([i, j])
                    found = True
                    break
            if found:
                break
    return number_vector

def final_code(number_vector: list, polybius_square: list, shift_rows: int, shift_cols: int) -> str:
    """Функция для финального шифрования, преобразовывая пары чисел
    в соответствии с шагом по строкам и столбцам
    """
    final_string = ""
    for pair in number_vector:
        i, j = pair[0], pair[1]
        new_i = (i + shift_rows) % 5
        new_j = (j + shift_cols) % 5
        buffer = polybius_square[new_i][new_j]
        if buffer == 'I/J':
            buffer = 'I'
        final_string += buffer
    return final_string

def build_mapping(square):
    """Создаёт словарь для быстрого поиска координат буквы
    в квадрате Полибия"""
    mapping = {}
    for i in range(5):
        for j in range(5):
            cell = square[i][j]
            if cell == 'I/J':
                mapping['I'] = (i, j)
                mapping['J'] = (i, j)
            else:
                mapping[cell] = (i, j)
    return mapping

def decrypt(encoded_text: str, shift_rows: int, shift_cols: int, square: list) -> str:
    """
    Дешифрует текст, зашифрованный сдвигом по строкам и столбцам
    в квадрате Полибия. Действует в обратном порядке с шифрованием.
    """
    mapping = build_mapping(square)
    result = []
    for ch in encoded_text:
        if ch not in mapping:
            continue 
        i_enc, j_enc = mapping[ch]
        i_orig = (i_enc - shift_rows) % 5
        j_orig = (j_enc - shift_cols) % 5
        cell = square[i_orig][j_orig]
        if cell == 'I/J':
            cell = 'I'
        result.append(cell)
    return ''.join(result)

def polybius_const(filename: str) -> list:
    """Читает файл с квадратом Полибия.
    Ожидается, что в файле через пробелы перечислены 25 символов/обозначений.
    Возвращает квадрат в виде списка списков 5x5.
    """
    content = intput_file(filename)
    items = content.split()
    if len(items) != 25:
        print(f"Warning: expected 25 elements in square file, got {len(items)}")
    square = []
    for i in range(5):
        row = items[i*5:(i+1)*5]
        square.append(row)
    return square

def parse_command_line():
    """Разбор аргументов командной строки с помощью argparse."""
    parser = argparse.ArgumentParser(
        description="Шифрование/дешифрование текста с использованием квадрата Полибия и сдвига по строкам/столбцам."
    )
    parser.add_argument(
        "square_file",
        help="Файл с квадратом Полибия (25 элементов, разделённых пробелами)"
    )
    parser.add_argument(
        "input_text_file",
        help="Файл с исходным текстом для шифрования"
    )
    parser.add_argument(
        "key_file",
        help="Файл с ключом: одно или два целых числа (сдвиг по строкам и сдвиг по столбцам), разделённых пробелами"
    )
    parser.add_argument(
        "output_decoded_file",
        help="Файл для записи расшифрованного текста (после проверки)"
    )
    parser.add_argument(
        "output_encoded_file",
        help="Файл для записи зашифрованного текста"
    )
    args = parser.parse_args()
    return (args.square_file, args.input_text_file, args.key_file,
            args.output_decoded_file, args.output_encoded_file)

def main():
    """
    Основная функция с вызовом раннее приведённых алгоритмов
    """
    (square_filename, text_filename, key_filename,
     decoded_filename, encoded_filename) = parse_command_line()

    polybius_square = polybius_const(square_filename)
    
    start_string = intput_file(text_filename)
    produce_string = normalize_str(start_string)
    
    number_vector = code_produce(produce_string, polybius_square)
    
    key_str = intput_file(key_filename).strip()
    parts = key_str.split()
    if not parts:
        shift_rows = shift_cols = 0
    else:
        shift_rows = int(parts[0])
        if len(parts) > 1:
            shift_cols = int(parts[1])
        else:
            shift_cols = 0 
    
    final_string = final_code(number_vector, polybius_square, shift_rows, shift_cols)
    
    decrypt_string = decrypt(final_string, shift_rows, shift_cols, polybius_square)
    
    output_file(decoded_filename, decrypt_string)
    output_file(encoded_filename, final_string)

if __name__ == "__main__":
    main()