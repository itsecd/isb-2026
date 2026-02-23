import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'lab_1', 'task2'))

from key import key 

def fileopen(filename: str) -> str:
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise e

def mapper(text: str):
    result = ""
    start_map = {}
    for i in text:
        if i in start_map:
            start_map[i]+=1/len(text)
        else:
            start_map[i]=1/len(text)
            
    start_map = {k: round(v, 5) for k, v in start_map.items()}
    sorted_map = sorted(start_map.items(), key=lambda item: item[1], reverse=True)
    for k, r in sorted_map:
        result += f"{k}: {r}\n"
    return result

def dechiper(text: str, key: map) -> str:
    result = ""

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
    parser.add_argument("--readfile", "-r", default="lab_1/task2/cod3.txt", type=str, help="Путь к файлу для чтения.")
    parser.add_argument("--writefile", "-w", default="lab_1/task2/dechiper.txt", type=str, help="Путь к файлу для записи результата.")
    parser.add_argument("--mapfile", "-m", default="lab_1/task2/map.txt", type=str, help="Путь к файлу для хранения частот.")
    args = parser.parse_args()

    try:
        file_writter(args.mapfile, mapper(fileopen(args.readfile)))
        file_writter(args.writefile, dechiper(fileopen(args.readfile), key))
    except Exception:
        print("Error.")

if __name__ == "__main__":
    main()