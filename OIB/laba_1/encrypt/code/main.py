import argparse 

from caesar import caesar_encrypt
from rw import read, write

def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-po", "--path_original", type=str, required=True, help="Путь к файлу для считывания.")
    parser.add_argument("-pe", "--path_encrypted", type=str, required=True, help="Путь к файлу для загрузки")
    parser.add_argument("-n", "--number", type=int, required=True, help="Число для сдвига.")

    args = parser.parse_args()
    return args.path_original, args.path_encrypted, args.number 

if __name__ == "__main__":
    path_original, path_encrypted, number = parser_args()

    text = read(path_original)

    encrypted_text = caesar_encrypt(text, number)

    write(path_encrypted, encrypted_text)