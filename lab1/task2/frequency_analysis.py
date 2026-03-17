import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="input.txt")
    parser.add_argument("-o", "--output", default="output.txt")
    return parser.parse_args()

def read_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filename: str, content: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def find_frequencies(text: str) -> dict:
    result = dict()
    n = len(text)
    for char in text:
        if not result.__contains__(char):
            result[char] = 1
        else:
            result[char] += 1
    for key in result:
        result[key] /= n
    return result

def replace_symbols(text: str, to_replace: dict, hide: bool = False) -> str:
    result = list()
    for char in text:
        if char in to_replace:
            result.append(to_replace[char])
        else:
            result.append("-") if hide else result.append(char)
    return "".join(result)

def main():
    args = parse_args()
    text = read_file(args.input)
    print(find_frequencies(text))
    to_replace = {
        "О": " ",
        "7": "О"
    }
    print(replace_symbols(text, to_replace, 1))

if __name__ == "__main__":
    main()