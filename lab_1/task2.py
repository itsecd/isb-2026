import argparse


def fileopen(filename: str) -> str:
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise e


def dechiper(text: str) -> str:
    result = ""
    key = {
        "N" : " ",
        "=" : "О",
        "Й" : "Е"
    }
    for char in text:
        if char in key:
            char = key[char]
        result += char
    return result


def file_writter(filename: str, data: str) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data)
    except Exception as e:
        raise e


def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--readfile", "-r", default="lab_1/cod3.txt", type=str, help="Путь к файлу для чтения.")
    parser.add_argument("--writefile", "-w", default="lab_1/dechiper.txt", type=str, help="Путь к файлу для записи результата.")
    args = parser.parse_args()

    try:
        file_writter(args.writefile, dechiper(fileopen(args.readfile)))
    except Exception:
        print("Error.")

if __name__ == "__main__":
    main()