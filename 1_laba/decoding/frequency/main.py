from collections import Counter

from utils import read, write

path_text = input("Введите название файла для получения текста: ")
path_output = input("Введите название файла для ввода в файл: ")

text = read(path_text)

text_count = Counter(text)

count = sum(text_count.values())

for key in text_count:
    text_count[key] /= count

write(path_output, str(text_count))
