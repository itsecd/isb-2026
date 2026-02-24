ALPHABET_LOWERCASE = tuple('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
ALPHABET_UPPERCASE = tuple('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')


def ReadFile(filename: str) -> tuple[str]:
    """
    Reading text from a file. 
    """
    with open(filename, "r", encoding = "utf-8") as file:
        text = file.read()

    return text


def TrithemiusCipher(original_text: tuple[str], KEY: list[int]) -> list[str]:
    """ 
    Text encryption using a trithemius cipher.
    """
    alphabet = None
    encrypted_text = []
    key = 0
    
    for letter in original_text:
        if not letter.isalpha():
            encrypted_text.append(letter)
            continue

        alphabet = ALPHABET_LOWERCASE if letter.islower() else ALPHABET_UPPERCASE
        letter_index = alphabet.index(letter)
        new_letter_index = (letter_index + KEY[key]) % len(alphabet)
        letter = alphabet[new_letter_index]
        encrypted_text.append(letter)
        key = (key + 1) % len(KEY)
    
    return encrypted_text


def WriteFile(text: list[str], filename: str) -> None:
    """ 
    Writing to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for word in text:
            file.write(word)


def DecryptionTrithemiusCipher(encrypted_text: list[str], KEY: list[int]) -> list[str]:
    """ 
    Text decryption using a trithemius cipher.
    """
    alphabet = None
    decrypted_text = []
    key = 0
    
    for letter in encrypted_text:
        if not letter.isalpha():
            decrypted_text.append(letter)
            continue

        alphabet = ALPHABET_LOWERCASE if letter.islower() else ALPHABET_UPPERCASE
        letter_index = alphabet.index(letter)
        new_letter_index = (letter_index - KEY[key]) % len(alphabet)
        letter = alphabet[new_letter_index]
        decrypted_text.append(letter)
        key = (key + 1) % len(KEY)
    
    return decrypted_text


def TranslateTheKey(key_word: list[str]) -> list[int]:
    """ 
    Records the letter indexes of the key.
    """
    if not key_word:
        raise ValueError('"file does not contain a key"')

    KEY = []
    for letter in key_word:
        if not letter.isalpha() or letter.upper() not in ALPHABET_UPPERCASE:
            raise ValueError('not a valid key')
        
        index = ALPHABET_UPPERCASE.index(letter.upper()) + 1
        KEY.append(index)
    
    return KEY


def main():
    try:
        original_text = ReadFile('non_encrypted_text_task_1.txt')
        KEY = TranslateTheKey(ReadFile('task_1_key.txt'))
        encrypted_text = TrithemiusCipher(original_text, KEY)
        WriteFile(encrypted_text, 'task_1_result.txt')
        decrypted_text = DecryptionTrithemiusCipher(encrypted_text, KEY)
        WriteFile(decrypted_text, "check_task_1_result.txt")

    except FileNotFoundError:
        print("Error: file not found")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    main()

