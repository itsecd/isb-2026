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


def Decryption(encryted_text: tuple[str]) -> list[str]:
    """ 
    Decrypting the text.
    """
    key = {
        'Р': ' ',
        'Ё': 'и',
        'Д': 'в',
        'Ж': 'к',
        'Я': 'т',
        '3': 'е',
        '1': 'о',
        'U': 'с',
        '@': 'а',
        '<': 'ч',
        'Т': 'л',
        'Z': 'б',
        'К': 'м',
        '9': 'н',
        'П': 'ы',
        'N': 'д',
        'J': 'з',
        'О': 'ь',
        'ю': 'я',
        'F': 'у',
        'Y': 'ш',
        '%': 'ж',
        'Х': 'р',
        'г': 'x',
        's': 'п',
        '=': 'щ',
        'Й': 'ю',
        'G': 'ц',
        'Q': 'ф',
        'И': 'э',
        'i': 'г',
        'у': 'й'
        # I don't think that '-' might be 'ъ'(
    }
    decrypted_text = []

    for letter in encryted_text:
        if letter in key:
            decrypted_text.append(key[letter])
        else:
            decrypted_text.append(letter)

    return decrypted_text


def WriteFile(text: list[str], filename: str) -> None:
    """ 
    Writing to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for word in text:
            file.write(word)


def main():
    try:
        encrypted_text = ReadFile("cod22.txt")
        frequency_of_letters = CountTheFrequencyOfLetters(encrypted_text)
        print(frequency_of_letters)
        decrypted_text = Decryption(encrypted_text)
        WriteFile(decrypted_text, "cod22_result.txt")
    
    except FileNotFoundError:
        print("Error: file not found")


if __name__ == "__main__":
    main()