import argparse

from tabl_polybia import encrypt, decrypt
from utils import write, read


def parser_args():
    parser = argparse.ArgumentParser(description="Шифрование методом таблицы Полибия")
    parser.add_argument(
        "-pi",
        "--path_input",
        type=str,
        required=True,
        help="Путь к файлу для считывания",
    )
    parser.add_argument(
        "-po",
        "--path_output",
        type=str,
        required=True,
        help="Путь к файлу для загрузки",
    )
    parser.add_argument(
        "-d", "--decrypt", action="store_true", help="Режим дешифрования"
    )

    args = parser.parse_args()
    return args.path_input, args.path_output, args.decrypt


if __name__ == "__main__":
    path_input, path_output, is_decrypt = parser_args()

    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

    text = read(path_input)

    if is_decrypt:
        text_another = decrypt(alphabet, text)
    else:
        text_another = encrypt(alphabet, text)

    write(path_output, text_another)
