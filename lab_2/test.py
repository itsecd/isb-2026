import math
from scipy.special import gammaincc

def load_file(path:str)-> str:
    """
    чтение текста из файла
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def bit_frequency_test(text:str) -> float:
    p = 0
    s = 0
    n = 128
    for i in text:
        if i == "1":
            s += 1
        else:
            s -= 1
    
    s = abs(s) / n**0.5
    p = math.erfc(s/2**0.5)
    
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
    return 0

if __name__ == "__main__":
    main()