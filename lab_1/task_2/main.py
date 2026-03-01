from conf import INPUT

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
    
    encodeData = readFromFile(inputFile)

    print(f"[RUN] => encode data:\n{encodeData}")

    print("[RUN] => success completed!")

    return


if __name__ == "__main__":
    main()