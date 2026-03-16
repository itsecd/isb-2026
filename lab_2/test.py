import math
from scipy.special import gammaincc

from paths import PATH_TO_PY
from paths import PATH_TO_CPP
from paths import PATH_TO_JAVA
from paths import PATH_TO_DATA

def load_file(path:str)-> str:
    """
    чтение текста из файла
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def save_to_file(lang:str , test1:float,test2:float, test3:float, path:str )->None:
    with open(path, "a", encoding="utf-8") as f:
        line = f"{lang} \n Частотный побитовый тест: {test1} \n Тест на одинаковые подряд идущие биты: {test2} \n Тест на самую длинную последовательность единиц в блоке: {test3} \n\n"
        f.write(line)

def bit_frequency_test(text:str) -> float:
    p = 0
    s = 0
    n = len(text)
    for i in text:
        if i == "1":
            s += 1
        elif i == "0":
            s -= 1
    
    s = abs(s) / (n**0.5)
    p = math.erfc(s/(2**0.5))
    
    return p

def test_for_identical_consecutive_bits(text:str)-> float:
    c = 0
    p = 0
    v = 0
    n = 128
    for i in text:
        if i == "1":
            c += 1
    
    c = c / n
    
    if(abs(c - 0.5) < (2/n ** 0.5)):
        for i in range(n - 1):
            if(text[i] != text[i+1]):
                v += 1
        
        p = math.erfc((abs(v - (2*n*c*(1-c))))/(2*((2*n)**0.5)*c*(1-c)))
    else:
        p = 0
    return p
    
    
def longest_sequence_of_ones_in_a_block_test(text:str)-> float:
    m = 8
    n = 128
    v = [0, 0, 0, 0]
    p = 0
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    x = 0
    
    for i in range(n//m):
        block = text[i * m: (i+1)*m]
        max_count = 0
        count = 0
        for j in block:
            if j == "1":
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0
        
        if max_count <= 1:
            v[0] += 1
        elif max_count == 2:
            v[1] += 1
        elif max_count == 3:
            v[2] += 1
        else:
            v[3] += 1
    
    for i in range(4):
        x += (((v[i] - 16*pi[i])**2)/(16*pi[i]))
    
    p = gammaincc(1.5 , x/2)
    
    return p


    



def main() -> None:
    java_subsequence = load_file(PATH_TO_JAVA)
    java_test1 = bit_frequency_test(java_subsequence)
    java_test2 = test_for_identical_consecutive_bits(java_subsequence)
    java_test3 = longest_sequence_of_ones_in_a_block_test(java_subsequence)
    save_to_file("Java", java_test1, java_test2, java_test3, PATH_TO_DATA)
    
    
    
    py_subsequence = load_file(PATH_TO_PY)
    py_test1 = bit_frequency_test(py_subsequence)
    py_test2 = test_for_identical_consecutive_bits(py_subsequence)
    py_test3 = longest_sequence_of_ones_in_a_block_test(py_subsequence)
    save_to_file("Python", py_test1, py_test2, py_test3, PATH_TO_DATA)
    
    cpp_subsequence = load_file(PATH_TO_CPP)
    cpp_test1 = bit_frequency_test(cpp_subsequence)
    cpp_test2 = test_for_identical_consecutive_bits(cpp_subsequence)
    cpp_test3 = longest_sequence_of_ones_in_a_block_test(cpp_subsequence)
    save_to_file("CPP", cpp_test1, cpp_test2, cpp_test3, PATH_TO_DATA)
    
    
if __name__ == "__main__":
    main()