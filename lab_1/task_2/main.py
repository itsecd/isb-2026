import ast
from collections import Counter
from conf import INPUT, OUTPUT, KEY, OUTPUT_FREQUENCY


def decode(key: str, text: str) -> str:
    """
    Decode
    """
    if not key or not text:
        raise ValueError("[ERROR] => text or key are no valid")

    keyDict = ast.literal_eval(key)
    decodeData = "".join(keyDict.get(char, char) for char in text)
    return decodeData


def getFrequency(text: str) -> str:
    """
    Give frequency
    """
    if not text:
        raise ValueError("[ERROR] => text is no valid")

    textLength = len(text)
    simDict = Counter(text)

    freq = {char: count / textLength for char, count in simDict.items()}

    return str(dict(sorted(freq.items(), key=lambda item: item[1], reverse=True)))


def writeToFile(filePath: str, data: str) -> None:
    """
    Write to file
    """
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(data)

    except Exception as e:
        raise Exception(f"[ERROR] => something went wrong: {e}")


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


def main() -> None:
    """
    Main function
    """
    inputFile = INPUT
    outputFile = OUTPUT
    outputFrequencyFile = OUTPUT_FREQUENCY
    keyFile = KEY
    
    encodeData = readFromFile(inputFile)
    print(f"[RUN] => encode data:\n{encodeData}")

    writeToFile(outputFrequencyFile, getFrequency(encodeData))

    key = readFromFile(keyFile)
    print(f"[RUN] => key: \n{key}")

    decodeData = decode(key, encodeData)

    writeToFile(outputFile, decodeData)

    print("[RUN] => success completed!")

    return


if __name__ == "__main__":
    main()