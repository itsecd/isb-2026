from task_2_key import KEY

def ReadFile(filename: str) -> tuple[str]:
    """
    Reading text from a file. 
    """
    with open(filename, "r", encoding = "utf-8") as file:
        text = file.read()

    return text


def CountTheFrequencyOfLetters(text: tuple[str]) -> dict[str, int]:
    """
    calculating the frequency of occurrence of letters. 
    """
    frequency = {}

    for letter in text:
        frequency[letter] = frequency.get(letter, 0) + 1

    for letter in frequency:
        frequency[letter] = frequency[letter] / len(text)
    
    sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequency


def Decryption(encrypted_text: tuple[str], key: dict[str, str]) -> list[str]:
    """ 
    Decrypting the text.
    """
    decrypted_text = []

    for letter in encrypted_text:
        if letter in key:
            decrypted_text.append(key[letter])
        else:
            decrypted_text.append(letter)

    return decrypted_text


def WriteFile(data, filename: str) -> None:
    """ 
    Writing to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        if isinstance(data, dict):
            for key, value in data.items():
                file.write(f"{key} = {value}\n")
        
        elif isinstance(data, (list, tuple)):
            for char in data:
                file.write(char)


def main():
    try:
        encrypted_text = ReadFile("cod22.txt")
        frequency_of_letters = CountTheFrequencyOfLetters(encrypted_text)
        WriteFile(frequency_of_letters, "frequency_of_letters_task_2.txt")
        decrypted_text = Decryption(encrypted_text, KEY)
        WriteFile(decrypted_text, "cod22_result.txt")
    
    except FileNotFoundError:
        print("Error: file not found")


if __name__ == "__main__":
    main()