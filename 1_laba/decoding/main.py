import ast

from utils import read

path_text = input("Введите название файла с текстом: ")
path_key = input("Введите название файла с ключом: ")

cipher_text = read(path_text)
decrypt_key = ast.literal_eval(read(path_key))

plain_text = ""

for char in cipher_text:
    plain_text += decrypt_key.get(char, char)

print(plain_text)