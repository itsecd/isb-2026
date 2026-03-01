from conf import INPUT, OUTPUT, KEY, ALPHABET, SECKRET_KEY

def readFromFile(filePath: str) -> str:
    """read from file"""
    
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = f.read().strip()
            return data

    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] => file: \"{filePath}\" not found")

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")

def writeToFile(filePath: str, data: str) -> None:
    """write to file"""

    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(data)

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")

def main() -> None:

    inputFile = INPUT
    keyFile = KEY

    key = "".join([char.upper() for char in SECKRET_KEY if char.upper() in ALPHABET])

    data = readFromFile(inputFile)

    filterData = "".join([char.upper() for char in data if char.upper() in ALPHABET])

    writeToFile(keyFile, key)

    return

if __name__ == "__main__":
    main()