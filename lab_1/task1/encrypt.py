import argparse
from file_work import write_file, read_file


def input_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', '-k', help='путь к файлу с ключом (алфавитом)')
    parser.add_argument('--input', '-i', help='путь к входному файлу с текстом')
    parser.add_argument('--output', '-o', help='путь для сохранения зашифрованного текста')
    
    return parser.parse_args()


def find_pos(matrix: list[list], symb: str) -> str:
    """Данная функция ищет позицию символа в матрице"""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == symb.upper():
                return (str(i + 1) + str(j + 1))
    
    return None


def alphabet_to_matrix(key: str) -> list[list]:
    """Данная функция превращает набор символов в матрицу"""
    alph_list = list(key)

    matrix = [['' for _ in range(6)] for _ in range(6)]
    ind = 0

    for i in range(6):
        for j in range(6):
            if (ind < len(alph_list)):
                matrix[i][j] = alph_list[ind].upper()
                ind += 1
                

    return matrix


def encrypt(matrix: list[list], text: str, save_path: str) -> None:
    """Данная функция сохраняет зашифрованный текст в файл"""

    encrypted_text = ""

    for s in text:
        encrypted_text += find_pos(matrix, s)

    write_file(save_path, encrypted_text)


def decrypt(matrix: list[list], path: str) -> str:
    """Данная функция дешифрует тект"""

    encrypted_text = read_file(path)
    decrypted_text = ""

    for k in range(0, len(encrypted_text) - 1, 2):
        i, j = (int(encrypted_text[k]) - 1), (int(encrypted_text[k + 1]) - 1)
        decrypted_text += matrix[i][j]

    return decrypted_text


def main() -> None:
    args = input_parse()
    key_path, input_path, enc_path = args.key, args.input, args.output
    
    text = read_file(input_path).upper()
    key = read_file(key_path).upper()
    matrix = alphabet_to_matrix(key)

    encrypt(matrix, text, enc_path)
    print(decrypt(matrix, enc_path))


if __name__ == "__main__":
    main()