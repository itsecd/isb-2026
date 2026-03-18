import random
import time

def write_file(filename, data):
    '''Запись в файл'''
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)
    

def generator(filename):
    '''Генератор последовательности'''
    random.seed(time.time())
    text = ""
    for i in range(128):
        random_int = random.randint(0, 1)
        text += str(random_int)
    write_file(filename , text)


def main():
    '''Основная функция'''
    filename = "python_results.txt"
    generator(filename)
    print(4)
if __name__ == "__main__":
    main()