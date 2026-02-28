def vigenere_encrypt(plain_text, key):
    """Vigenere cipher"""
    encrypted_text= []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]


def create_key():
    """creating encryption key"""
    key = "ПЕПС"
    return key


def write_to_files(original_text, encrypted_text, key):
    """Function for writing to files"""

    with open('encrypted_text.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    
    with open('original_text', 'w', encoding='utf-8') as file:
        file.write(original_text)
 
    with open('encryption_key.txt', 'w', encoding='utf-8') as file:
        file.write(f"Ключ шифрования: {key}\n")
        file.write(f"Длина ключа: {len(key)}\n")

def main():
    plain_text = ""
    plain_text = ' '.join(plain_text.split())
    key = create_key()

    encrypted_text = vigenere_encrypt(plain_text, key)

    write_to_files(plain_text, encrypted_text, key)
