Alphabet_rus = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
Alphabet_size = len(Alphabet_rus)

def caesar_encrypt(text: str, key: int) -> str:
    encrypted_text = ""
    key = key % Alphabet_size

    for char in text.upper():
        if char in Alphabet_rus:
            orig_index = Alphabet_rus.index(char)
            new_index = (key + orig_index) % Alphabet_size
            encrypted_text += Alphabet_rus[new_index]
        else:
            encrypted_text += char
            
    return encrypted_text 