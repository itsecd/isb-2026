import math
from scipy.special import gammaincc


def bit_frequency_test(bitstring: str) -> float:
    """
    Функция для частотного побитового теста
    """
    sumn = (bitstring.count('1')-bitstring.count('0'))/math.sqrt(len(bitstring))
    pvalue = math.erfc(abs(sumn)/math.sqrt(2))
    return pvalue


def consecutive_bits_test(bitstring: str) -> float:
    """
    Функция для теста на одинаковые подряд идущие биты
    """
    pvalue = 0
    xi = bitstring.count('1')/len(bitstring)
    if (abs(xi-0.5) < (2/math.sqrt(len(bitstring)))):
        vn = 1
        for i in range(len(bitstring)-1):
            if (bitstring[i]!=bitstring[i+1]):
                vn += 1
        pvalue = math.erfc(abs(vn-2*len(bitstring)*xi*(1-xi))/(2*math.sqrt(2*len(bitstring))*xi*(1-xi)))
    return pvalue


def longest_sequence_test(bitstring: str) -> float:
    """
    Функция для теста на самую длинную последовательность единиц в блоке
    """
    pvalue = 0
    blocks = [""]*16
    for i in range(0,8):
        blocks[0]+=(bitstring[i])
    for i in range(8,len(bitstring)):
        blocks[i//8]+=(bitstring[i])
    v1, v2, v3, v4 = 0, 0, 0, 0
    for block in blocks:
        lmax, lcurrent = 0, 0
        for i in range(len(block)-1):
            if(block[i]!=block[i+1]):
                lmax = max(lmax, lcurrent)
                lcurrent = 0
            else:
                lcurrent += 1
        if (lmax <= 1):
            v1 += 1
        elif (lmax == 2):
            v2 += 1
        elif (lmax == 3):
            v3 += 1
        else:
            v4 += 1
    chi = ((v1-16*0.2148)**2)/(16*0.2148) + ((v2-16*0.3672)**2)/(16*0.3672) + ((v3-16*0.2305)**2)/(16*0.2305) + ((v4-16*0.1875)**2)/(16*0.1875)
    pvalue = gammaincc(1.5,(chi/2))
    return pvalue


def run_tests(bitstring: str) -> tuple[float, float, float]:
    """
    Функция для проведения тестов над псч
    """
    frequency = bit_frequency_test(bitstring)
    consecutive = consecutive_bits_test(bitstring)
    sequence = longest_sequence_test(bitstring)
    return frequency, consecutive, sequence


def write_results(prng_name: str, filename: str, bitstring: str, mode: str) -> None:
    """
    Функция для записи результатов тестов
    """
    test_results = run_tests(bitstring)
    with open(filename, mode, encoding="utf-8") as f:
        f.write("ГПСЧ языка: "+prng_name+"\n")
        f.write("Частотный побитовый тест "+str(test_results[0])+"\n")
        f.write("Тест на одинаковые подряд идущие биты: "+str(test_results[1])+"\n")
        f.write("Тест на самую длинную последовательность единиц в блоке "+str(test_results[2])+"\n\n")


def write_results_nooverwrite(prng_name: str, filename: str, bitstring: str) -> None:
    """
    Функция для записи результатов тестов
    """
    test_results = run_tests(bitstring)
    with open(filename, "a", encoding="utf-8") as f:
        f.write("ГПСЧ языка: "+prng_name+"\n")
        f.write("Частотный побитовый тест "+str(test_results[0])+"\n")
        f.write("Тест на одинаковые подряд идущие биты: "+str(test_results[1])+"\n")
        f.write("Тест на самую длинную последовательность единиц в блоке "+str(test_results[2])+"\n\n")


def main() -> None:
    """
    Главная фунцкия, осуществляющая загрузку псч, проведение тестов и запись результатов
    """
    with open("python_string.txt", "r", encoding="utf-8") as fp:
        py_string = fp.read()
    write_results("Python", "results.txt", py_string, "w")
    with open("cpp_string.txt", "r", encoding="utf-8") as fc:
        cpp_string = fc.read()
    write_results("C++", "results.txt", cpp_string, "a")
    with open("java_string.txt", "r", encoding="utf-8") as fj:
        java_string = fj.read()
    write_results("Java", "results.txt", java_string, "a")


if __name__ == "__main__":
    main()