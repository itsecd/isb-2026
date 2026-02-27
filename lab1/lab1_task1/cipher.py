import argparse


def read_file (file_name: str) -> str:
    """
    читает текст из файла
    """
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()
        return text


def column_transposition (text: str, key: str) -> str:
    """
    шифрует текст при помощи метода постолбцовой транспозиции
    """
    text = text.replace(" ", "_")
    n = len(key)

    remainder = len(text) % n
    if remainder > 0:
        text += "_" * (n-remainder)

    matrix = []
    while len(text) > 0:
        row = text[:n]
        matrix.append(row)
        text = text[n:]

    index_in_key = []
    for i in range(n):
        index_in_key.append((key[i], i))

    index_in_key.sort()

    alphabet_order = [0] * n 
    alphabet_number = 1

    for pair in index_in_key:
        position_in_key = pair[1]
        alphabet_order[position_in_key] = alphabet_number
        alphabet_number += 1

    alphabet_and_column = []
    for i in range(n):
        alphabet_and_column.append((alphabet_order[i], i))
    
    alphabet_and_column.sort()

    result = ""
    for pair in alphabet_and_column:
        column_index = pair[1]
        for row in matrix:
            result += row[column_index]

    final_text = ""
    counter = 0

    for character in result:
        final_text += character
        counter += 1
        if counter == 5:
            final_text += " "
            counter = 0

    return final_text


def column_transposition_decipher (text: str, key: str) -> str:
    """
    дешифрует текст, зашифрованный методом постолбцовой транспозиции
    """
    text = text.replace(" ", "")
    n = len(key)
    number_rows = len(text) // n

    index_in_key = []
    for i in range(n):
        index_in_key.append((key[i], i))
    
    index_in_key.sort()

    alphabet_order = [0] * n 
    alphabet_number = 1
    for pair in index_in_key:
        position_in_key = pair[1]
        alphabet_order[position_in_key] = alphabet_number
        alphabet_number += 1

    alphabet_and_column = []
    for i in range(n):
        alphabet_and_column.append((alphabet_order[i], i))
    
    alphabet_and_column.sort()

    matrix = []
    for i in range(number_rows):
        matrix.append([''] * n)

    current_index = 0
    for pair in alphabet_and_column:
        column_index = pair[1]
        for row_index in range(number_rows):
            matrix[row_index][column_index] = text[current_index]
            current_index += 1

    result = ""
    for row in matrix:
        result += "".join(row)

    result = result.replace("_", " ").rstrip("")
    return result


def write_file (text:str, output_file: str) -> None:
    """
    записывает текст в файл
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_file_name', type=str, default='original_text.txt', help='name of input file')
    parser.add_argument("-c", '--cipher_file_name', type=str, default='cipher_text.txt', help='name of cipher file')
    parser.add_argument("-d", '--decipher_file_name', type=str, default='decipher_text.txt', help='name of decipher file')
    parser.add_argument("-k", '--key', type=str, default='key.txt', help='cipher key')
    args = parser.parse_args()
    
    print(f"The name of input file is: {args.input_file_name}")
    print(f"The name of file with key is: {args.key}")
    print(f"The name of cipher file is: {args.cipher_file_name}")
    print(f"The name of decipher file is: {args.decipher_file_name}")

    try:
        text = read_file(args.input_file_name)
        key = read_file(args.key)
        cipher_text = column_transposition(text, key)
        write_file(cipher_text, args.cipher_file_name)
        decipher_text = column_transposition_decipher(cipher_text, key)
        write_file(decipher_text, args.decipher_file_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__" :
    main()