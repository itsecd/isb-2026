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
    result = ""
    for char in text:
        if char in map:
            result+=map[char]
        elif char == ' ':
            result+= ' '
        else:
            result+= char 
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description='Polibius encode')
    parser.add_argument('--input_file', required=True, help='file with text')
    parser.add_argument('--key', required=True, help='key for encode')
    parser.add_argument('--output_file', required=True, help='file for encode text')
    args = parser.parse_args()
    text = read_text(args.input_file)
    key = pd.read_excel(args.key)
    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(encode_polibius(text, key))    
            print(f"Your text is encode")
    except PermissionError:
        print(f"Permission denied")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)
        
if __name__ == "__main__":
    main()