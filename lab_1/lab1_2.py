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


def counter(text: str)-> dict:
    """
    подсчет того сколько раз символ встречается в тексте
    """
    counter = {}
    for char in text:
        if char in counter:
            counter[char] += 1
        else:
            counter[char] = 1
    
    return counter


def main():
    return 0    