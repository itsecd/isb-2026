from conf import INPUT, OUTPUT, KEY, ALPHABET, SECKRET_KEY


def readFromFile(filePath: str) -> str:
    """
    Read from file
    """
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = f.read().strip()
            return data

    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] => file: \"{filePath}\" not found")

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")


def writeToFile(filePath: str, data: str) -> None:
    """
    Write to file
    """
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(data)

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")


def encode(text: str, key: str) -> str:
    """
    Encode vigenere cipher
    """
    if not key:
        raise ValueError("[ERROR] => key has no valid simbol")

    result = []
    keyIndex = 0

    for char in text:
        indexFirst = ALPHABET.index(key[keyIndex % len(key)])
        indexSecond = ALPHABET.index(char)
        indexNew = (indexSecond + indexFirst) % len(ALPHABET)
        result.append(ALPHABET[indexNew])
        keyIndex += 1

    return "".join(result)


def decode(text: str, key: str) -> str:
    """
    Decode vigenere cipher
    """
    if not key:
        raise ValueError("[ERROR] => key has no valid simbol")

    result = []
    keyIndex = 0

    for char in text:
        indexFirst = ALPHABET.index(key[keyIndex % len(key)])
        indexSecond = ALPHABET.index(char)
        indexNew = (indexSecond - indexFirst) % len(ALPHABET)
        result.append(ALPHABET[indexNew])
        keyIndex += 1

    return "".join(result)


def main() -> None:
    """
    Main function
    """
    inputFile = INPUT
    outputFile = OUTPUT
    keyFile = KEY

    key = "".join([char.upper() for char in SECKRET_KEY if char.upper() in ALPHABET])

    data = readFromFile(inputFile)

    filterData = "".join([char.upper() for char in data if char.upper() in ALPHABET])

    encryptedData = encode(filterData, key)
    decryptedData = decode(encryptedData, key)

    if filterData != decryptedData:
        print("[ERROR] => the original text is`t equal to the decrypted text")
        return

    writeToFile(outputFile, encryptedData)
    writeToFile(keyFile, key)

    print("[RUN] => success completed!")

    return


if __name__ == "__main__":
    main()