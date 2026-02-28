
def load_file(path:str)-> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def save_file(path:str, text:str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    
    
    
def clear_key(key:str, alfovit: str):
    clean_key = []
    
    for letter in key:
        if letter in alfovit:
            clean_key.append(letter)
    
    return clean_key

def vigener_cipher(text: str, key: str, alfovit: str, mode:bool) -> str:
    """
    
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



def main():
    alfovit = sorted("йцукенгшщзхъфывапролджэячсмитьбюёЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮqwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    return 0