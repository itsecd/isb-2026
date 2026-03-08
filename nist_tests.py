import argparse
import math
from scipy.special import gammaincc
import csv

def read_data(filenamesequence):
    """
    Чтение файла
    """
    with open(filenamesequence,"r",encoding="utf-8") as file:
        sequence=file.read()
        return sequence

def frequency_bitwise_test(data):
    """
    Частотный побитовый тест
    """
    sum=0
    for i in data:
        if i==1:
            sum+=1
        else:
            sum-=1
    s=abs(sum)/math.sqrt(len(data))
    p=math.erfc(s/math.sqrt(2))
    return p

def test_identical_consecutive_bits(data):
    """
    Тест на одинаковые подряд идущие биты
    """
    sum=0
    for i in data:
        sum+=i
    e=sum/len(data)
    p=0
    if abs(e-0.5)<(2/math.sqrt(len(data))):
        r=0
        for i in range(len(data)-1):
            if data[i]==data[i+1]:
                r+=0
            else:
                r+=1
        p=math.erfc(abs(r-2*len(data)*e*(1-e))/(2*math.sqrt(2*len(data))*e*(1-e)))
        return p
    else:
        return p

def longest_sequence_units_block(data):
    """
    Тест на самую длинную последовательность единиц в блоке
    """
    data_parts=[data[i:i+8] for i in range(0,128,8)]
    len_parts=[]
    for i in range(len(data_parts)):
        max_len = 0
        current_len = 0
        for j in range(8):
            if data_parts[i][j]==1:
                current_len+=1
                max_len=max(max_len,current_len)
            else:
                current_len=0
        len_parts.append(max_len)
    len_blocks=[0,0,0,0]
    for i in len_parts:
        if i<=1:
            len_blocks[0]+=1
        if i==2:
            len_blocks[1]+=1
        if i==3:
            len_blocks[2]+=1
        if i>=4:
            len_blocks[3]+=1
    pi_list=[0.2148,0.3672,0.2305,0.1875]
    x=0
    for i in range(4):
        x+=((len_blocks[i]-16*pi_list[i])**2)/(16*pi_list[i])
    p = gammaincc(3/2, x/2)
    return p

def check_p(p):
    """
    Функция проверки значения p
    """
    if p>=0.01:
        return True
    else:
        return False

def nist_tests(vec,language):
    """
    Функция проведения тестов
    """
    result=[]

    p_1=frequency_bitwise_test(vec)
    if check_p(p_1):
        result.append([f"{language}","Частотный побитовый тест",f"{p_1}","Пройден"])
    else:
        result.append([f"{language}","Частотный побитовый тест",f"{p_1}","Провален"])

    p_2=test_identical_consecutive_bits(vec)
    if check_p(p_2):
        result.append([f"{language}","Тест на одинаковые подряд идущие биты",f"{p_2}","Пройден"])
    else:
        result.append([f"{language}","Тест на одинаковые подряд идущие биты",f"{p_2}","Провален"])

    p_3=longest_sequence_units_block(vec)
    if check_p(p_3):
        result.append([f"{language}","Тест на самую длинную последовательность единиц в блоке",f"{p_3}","Пройден"])
    else:
        result.append([f"{language}","Тест на самую длинную последовательность единиц в блоке",f"{p_3}","Провален"])

    return result

def write_result(result,filenameoutput):
    """
    Функция получения файла отчёта
    """
    with open(filenameoutput, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in result:
                for element in row:
                    writer.writerow(element)

def to_list(string):
    """
    Функция перевода строки в числовой вектор
    """
    return [int(char) for char in string]

def parsing():
    """
    Получение аргументов командной строки
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("filenamecpp",type=str,help="Введите названия файла с исходной последовательностью")
    parser.add_argument("filenamejava",type=str,help="Введите названия файла с исходной последовательностью")
    parser.add_argument("filenamepython",type=str,help="Введите названия файла с исходной последовательностью")
    parser.add_argument("filenameoutput",type=str,help="Введите названия файла вывода")
    args=parser.parse_args()
    return args.filenamecpp,args.filenamejava,args.filenamepython,args.filenameoutput

def main():
    filenamecpp,filenamejava,filenamepython,filenameoutput=parsing()

    data_cpp=read_data(filenamecpp)
    data_java=read_data(filenamejava)
    data_python=read_data(filenamepython)

    cpp_vec=to_list(data_cpp)
    java_vec=to_list(data_java)
    python_vec=to_list(data_python)

    result=[]

    result.append(nist_tests(cpp_vec,"C++"))
    result.append(nist_tests(java_vec,"Java"))
    result.append(nist_tests(python_vec,"Python"))

    write_result(result,filenameoutput)

if __name__=="__main__":
    main()