from collections import Counter

from rw import read, write

path_text = input("Введите название файла нужного для анализа текста: ")
path_analiz = input("Введите название файла для частот: ")

text = read(path_text)

text_count = Counter(text)

count = sum(text_count.values())

for key in text_count:
    text_count[key] /= count

write(path_analiz, str(text_count))