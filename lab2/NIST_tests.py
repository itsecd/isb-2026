import math
from scipy.special import gammaincc # pyright: ignore[reportMissingImports]
import os


def file_read(file: str) -> str:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Файл не найден: {file}")
    with open (f"{file}", mode='r', encoding='utf-8') as f:
        data = f.read().strip()
    if not data:
        raise ValueError("{file} не содержит данных")
    return data


def frequency_bitwise_analysis(data: str) ->float:
    '''Частотный побитовый анализ'''
    x = [1 if bit == '1' else -1 for bit in data]
    S = sum(x)
    S_n = S/math.sqrt(len(data))
    p = math.erfc(abs(S_n)/math.sqrt(2))
    return p


def consecutive_identical_bits(data: str) -> float:
    '''Тест на одинаковые подряд идущие биты'''
    eps = [int(bit) for bit in data]
    zeta = sum(eps)/len(data)
    if (abs(zeta - 0.5) > 2/math.sqrt(len(data))):
        return 0.0
    V_n = 0
    for i in range (len(data)-1):
        if eps[i] != eps[i+1]:
            V_n +=1
    P = math.erfc(abs(V_n - 2* len(data)*zeta*(1-zeta))/(2*math.sqrt(2*len(data))*zeta*(1-zeta)))
    return P


def longest_sequence(data: str) -> float:
    '''Тест на самую длинную последовательность единиц в блоке'''
    v = [0]*4
    temp = 0
    maxi = 0
    k = 0

    for i in data:
        if i =='1':
            temp +=1
        else:
            maxi = max(maxi, temp)
            temp = 0
        k +=1
        if k == 8:
            maxi = max(maxi, temp)
            if maxi <= 1:
                v[0] += 1
            elif maxi == 2:
                v[1] += 1
            elif maxi == 3:
                v[2] += 1
            else:
                v[3] += 1
            maxi = k = temp = 0
    p = [0.2148, 0.3672, 0.2305, 0.1875]
    chi_sq = 0.0
    for i in range (4):
        chi_sq += ((v[i]-16*p[i])**2)/(16*p[i])
    return gammaincc(3/2, chi_sq/2)


def check(p1: float, p2: float, p3: float) -> str:
    '''проверка на успех тестов'''
    res = ''
    if p1 >= 0.01:
        res += f'Частотный побитовый анализ пройден {p1: .3f}\n'
    else:
        res += f'Частотный побитовый анализ не пройден {p1: .3f}\n'{[]}
    
    if p2 >= 0.01:
        res += f'Тест на одинаковые подряд идущие биты пройден {p2: .3f}\n'
    else:
        res += f'Тест на одинаковые подряд идущие биты не пройден {p2: .3f}\n'
    
    if p3 >= 0.01:
        res += f'Тест на самую длинную последовательность единиц в блоке пройден {p3: .3f}\n'
    else:
        res += f'Тест на самую длинную последовательность единиц в блоке не пройден {p3: .3f}\n'
    
    return res


def result(file: str, res1: str, res2:str, res3: str) -> None:
    '''Запись результатов в файл'''
    with open (file, mode='w', encoding='utf-8') as f:
        f.write("ГСПЧ на C++:\n"+res1)
        f.write("\n\nГСПЧ на Python:\n"+res2)
        f.write("\n\nГСПЧ на java:\n"+res3)


def main() -> None:
    data_cpp = file_read("out_cpp.txt")
    data_py = file_read("out_py.txt")
    data_java = file_read("out_java.txt")
    result("result.txt",
           check(frequency_bitwise_analysis(data_cpp), consecutive_identical_bits(data_cpp), longest_sequence(data_cpp)),
           check(frequency_bitwise_analysis(data_py), consecutive_identical_bits(data_py), longest_sequence(data_py)),
            check(frequency_bitwise_analysis(data_java), consecutive_identical_bits(data_java), longest_sequence(data_java)))


if __name__ == "__main__":
    main()