Alphabet_rus = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
Alphabet_size = len(Alphabet_rus)

def caesar_encrypt(text: str, key: int) -> str:
    """Функция-реализация шифра Цезаря."""
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

def caesar_decrypt(text: str, key: int) -> str:
    """Функция дешифратор шифра Цезаря."""
    decryption_key = Alphabet_size - (key % Alphabet_size)
    return caesar_encrypt(text, decryption_key)