import argparse

import pandas as pd

def read_text(filename: str) -> str:
    """ function for read from file """
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found")
        exit(2)
    except PermissionError:
        print(f"Premision denied")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)

    
def encode_polibius(text: str, key: pd.DataFrame) -> str:
    """ encode text function """
    text = text.upper()
    rows, cols = key.shape
    map = {}
    for i in range(rows):
        for j in range(cols):
            cell = key.iloc[i, j]
            if cell and str(cell).strip():
                map[cell] = f"{i+1}{j+1}"
    result = []
    for char in text:
        if char in map:
            result.append(map[char])
        elif char == ' ':
            result.append(' ')
        else:
            result.append(char)
    return ' '.join(result)

def main() -> None:
    print()    

if __name__ == "__main__":
    main()