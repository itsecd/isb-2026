import argparse

def parse_arguments():
    """
    парсинг командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_a", help="Путь к тексту")
    parser.add_argument("file_b", help="Путь к ключу")
    parser.add_argument("file_c", help="Путь к результату")
    parser.add_argument("mode", help="Выбор шифровки(1) или дешифровки(0)")
    return parser.parse_args()

def load_file(path:str)-> str:
    """
    чтение текста из файла
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def save_file(path:str, text:str)-> None:
    """
    сохранение текста в файл
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    

def clear_key(key:str, alfovit: str) -> list:
    """
    очистка ключа от ненужных символов
    """
    clean_key = []
    
    for letter in key:
        if letter in alfovit:
            clean_key.append(letter)
    
    return clean_key

def vigener_cipher(text: str, key: str, alfovit: str, mode:bool) -> str:
    """
    в зависимости от mode либо шифрует, либо дешифрует текст
    """
    result = ""
    key = clear_key(key, alfovit)
    
    letters = {letter: ind for ind, letter in enumerate(alfovit)}
    indexs = {ind: letter for ind, letter in enumerate(alfovit)}
    
    key_ind = 0
    key_len = len(key)
    #(ind + key_ind) % len)alfovit
    for char in text:
        if char in letters:
            char_ind = letters[char]
            key_char = key[key_ind]
            shift = letters[key_char]
            if(mode):
                cipher_ind = (char_ind + shift) % len(alfovit)
            else:
                cipher_ind = (char_ind - shift) % len(alfovit)
                
            result += indexs[cipher_ind]  
                
            if(key_ind == key_len - 1):
                key_ind = 0
            else:
                key_ind += 1
        else:
            result += char
    
    return result



def main() -> None:
    """
    основная функция программы
    """
    args = parse_arguments()
    
    text = load_file(args.file_a)
    key = load_file(args.file_b)
    
    alfovit = sorted("йцукенгшщзхъфывапролджэячсмитьбюёЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮqwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    
    if(args.mode == "1"):
        mode = True
    else:
        mode = False
        
    result = vigener_cipher(text, key, alfovit, mode)
    save_file(args.file_c, result)
    


if __name__ == "__main__":
    main()