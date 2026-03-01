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
        


def dict_to_file(path:str, frq:dict)->None:
    """
    сохранение словаря в файл
    """
    with open(path, "w", encoding="utf-8") as f:
        for char in frq:
            val = frq[char]
            line = f"{char}: {val} \n"
            f.write(line)
            
def load_key(path:str)-> dict:
    """
    чтение ключа из файла
    """
    key = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            char_from = line[0]
            char_to = line[1]
            key[char_from] = char_to
    return key
    

            
def counter(text: str)-> dict:
    """
    подсчет того сколько раз символ встречается в тексте
    """
    counter = {}
    for char in text:
        if char == "\n": 
            continue
        if char in counter:
            counter[char] += 1
        else:
            counter[char] = 1
    
    return counter

def frequency(counter: dict, text: str) -> dict:
    """
    подсчет частоты встречи символа в тексте
    """
    len_text = len(text)
    frequency = {}
    for char in counter:
          frequency[char] = counter[char]/len_text
    return frequency

def decode(text:str, key:dict)->str:
    """
    декодинг по ключу
    """
    result_text = ""
    
    for char in text:
        if char in key:
            result_text += key[char]
        else:
            result_text += char
    
    return result_text
    

def main():
    text = load_file("cod23.txt")
    key = load_key("key2.txt")
    
    result = decode(text, key)
    save_file("result3.txt", result)
    

    
    
    
    
    
    
if __name__ == "__main__":
    main()