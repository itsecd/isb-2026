import json
from rw import read, write 

def decrypt(encrypted_text: str, key: dict) -> str:
    d_text = ""
    for char in encrypted_text:
        d_text += key.get(char, char)

    d_text = d_text.upper()
    return d_text

if __name__ == "__main__":

    path_original = input("Введите название файла с текстом: ")
    path_key = input("Введите название файла с ключом дешифровки: ")
    path_output_file = input("Введите название файла для сохранения расшифрованного текста: ")
    encrypted_text = read(path_original)
    key_content = read(path_key)
    key = json.loads(key_content)
    decrypted_text = decrypt(encrypted_text, key)
    write(path_output_file, decrypted_text)