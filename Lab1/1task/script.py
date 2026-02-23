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

def code_produce(produce_string: str,polybius_square: list) -> list:
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

def final_code(number_vector: list,polybius_square: list, shift: int)->str:
    """Функция для финального шифрования, преобразовывая пары чисел
    в соответствии с шагом
    """
    final_string = ""
    for pair in number_vector:
        i, j = pair[0], pair[1]
        new_i = (i + shift) % 5
        buffer = polybius_square[new_i][j]
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

def decrypt(encoded_text: str, shift: int, square: list) -> str:
    """
    Дешифрует текст, зашифрованный сдвигом по строкам в квадрате Полибия
    Действует в обратном порядке с шифрованием
    Перебирает символы(на всякий случай сравнивает с алфавитом,
    для универсальности функции)
    Затем ищет правильную букву, относительно заданной и шага
    """
    mapping = build_mapping(square)
    result = []
    for ch in encoded_text:
        if ch not in mapping:
            continue 
        i_enc, j = mapping[ch]
        i_orig = (i_enc - shift) % 5
        cell = square[i_orig][j]
        if cell == 'I/J':
            cell = 'I'
        result.append(cell)
    return ''.join(result)



polybius_square = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I/J', 'K'],
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
    ]
def main():
    """
    Основная функция с вызовом раннее приведённых алгоритмов
    """
    start_string = intput_file("text.txt")
    produce_string=normalize_str(start_string)
    number_vector=code_produce(produce_string,polybius_square)
    key_str = intput_file("key.txt").strip()
    shift = int(key_str) if key_str else 1
    final_string=final_code(number_vector,polybius_square,shift)
    decrypt_string=decrypt(final_string,shift,polybius_square)
    output_file("decoded.txt", decrypt_string)
    output_file("code.txt", final_string)


if __name__ == "__main__":
    main()