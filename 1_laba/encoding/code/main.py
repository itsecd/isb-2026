import argparse

from tabl_polybia import encrypt
from utils import write, read

def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pi", "--path_input", type=str, required=True, help="Путь к файлу для считывания")
    parser.add_argument("-po", "--path_output", type=str, required=True, help="Путь к файлу для загрузки")

    args = parser.parse_args()
    return args.path_input, args.path_output

if __name__ == "__main__":
    path_input, path_output = parser_args()
    
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

    text = read(path_input)

    text_another = encrypt(alphabet, text)

    write(path_output, text_another)