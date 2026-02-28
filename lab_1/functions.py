def vigenere_encrypt(text, key):
    """Vigenere cipher"""

    ru_upper = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    encrypted_text= []
    key_length = len(key)
    #key_as_int = [ord(i) for i in key]

    for i in range(len(text)):
        current_char = text[i]
        
        char_index=-1
        for j in range(len(ru_upper)):
            if ru_upper[j] == current_char:
                char_index = j
                break
        if char_index != -1:
            key_char = key[i % key_length]
            key_index = -1
            for j in range(len(ru_upper)):
                if ru_upper[j] == key_char:
                    key_index = j
                    break


            new_index = (char_index + key_index) % 33
            encrypted_text += ru_upper[new_index]
        else:
            encrypted_text += current_char

    return ''.join(encrypted_text)


def create_key():
    """Creating encryption key"""
    key = "ПЕПС"
    return key


def write_to_files(original_text, encrypted_text, key):
    """Function for writing to files"""

    with open('encrypted_text.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    
    with open('original_text.txt', 'w', encoding='utf-8') as file:
        file.write(original_text)
 
    with open('encryption_key.txt', 'w', encoding='utf-8') as file:
        file.write(f"Ключ шифрования: {key}\n")
        file.write(f"Длина ключа: {len(key)}\n")

def main():
    plain_text = "вавВВА"
    plain_text = ' '.join(plain_text.split())
    key = create_key()

    encrypted_text = vigenere_encrypt(plain_text, key)

    write_to_files(plain_text, encrypted_text, key)
