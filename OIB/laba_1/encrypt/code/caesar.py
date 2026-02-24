import const

def caesar_encrypt(text: str, key: int) -> str:
    """Функция-реализация шифра Цезаря."""
    encrypted_text = ""
    key = key % const.ALPHABET_SIZE

    for char in text.upper():
        if char in const.ALPHABET_RUS:
            orig_index = const.ALPHABET_RUS.index(char)
            new_index = (key + orig_index) % const.ALPHABET_SIZE
            encrypted_text += const.ALPHABET_RUS[new_index]
        else:
            encrypted_text += char
            
    return encrypted_text 

def caesar_decrypt(text: str, key: int) -> str:
    """Функция дешифратор шифра Цезаря."""
    decryption_key = const.ALPHABET_SIZE - (key % const.ALPHABET_SIZE)
    return caesar_encrypt(text, decryption_key)