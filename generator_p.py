import argparse
import random

def write_data(data,filenameoutput):
     with open(filenameoutput,mode="w", newline="",encoding="utf-8") as file:
        file.write(data)

def generate(filenameoutput):
    data=""
    for i in range(128):
        data+=str(random.randint(0, 1))
    write_data(data,filenameoutput)

def parsing():
    """
    Получение аргументов командной строки
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("filenameoutput",type=str,help="Введите названия файла вывода")
    args=parser.parse_args()
    return args.filenameoutput

def main():
    filenameoutput=parsing()
    generate(filenameoutput)

if __name__=="__main__":
    main()