from collections import Counter
import os
import sys

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root)

from utils import read, write

def count_freq(text: str):
    text_count = Counter(text)

    count = sum(text_count.values())

    for key in text_count:
        text_count[key] /= count

    return text_count

if __name__ == "__main__":
    path_text = input("Введите название файла для получения текста: ")
    path_output = input("Введите название файла для ввода в файл: ")

    text = read(path_text)

    text_count = count_freq(text)

    write(path_output, str(text_count))