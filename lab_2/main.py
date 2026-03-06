import math
import scipy.special as sp

import work_file


def frequency_bit_test(binary_str: str) -> float:
    """
    """
    stat = 1 / math.sqrt(len(binary_str)) * (binary_str.count("1") - binary_str.count("0"))
    p_value = math.erfc(stat / math.sqrt(2))
    return p_value

def  identical_consecutive_bit_test(binary_str: str) -> float:
    """
    """
    n = len(binary_str)
    xi = binary_str.count("1") / n
    if abs(xi - 0.5) >= (2 / math.sqrt(n)):
        return 0
    V_n = 0
    for i in range(n - 1):
        if(binary_str[i] != binary_str[i + 1]):
            V_n += 1
    
    p_value = math.erfc(abs(V_n - 2 * n * xi * (1 - xi)) / (2 * math.sqrt(2 * n) * xi * (1 - xi)))

    return p_value


def  longest_sequence_in_block(binary_str: str, p: list) -> float:
    """
    """

    blocks = []
    n = len(binary_str)
    for i in range(0, n, 8):
        block = binary_str[i: i + 8]
        blocks.append(block)
    v = [0, 0, 0, 0]
    for block in blocks:
        max_run = 0
        cur_len = 0
        for j in block:
            if j == "1":
                cur_len += 1
                max_run = max(max_run, cur_len)
            else:
                cur_len = 0
        match max_run:
            case 0 | 1 : v[0] += 1
            case 2     : v[1] += 1
            case 3     : v[2] += 1
            case _ if max_run >= 4: v[3] += 1
    
    Xi_kv = sum(((v[i] - 16 * p[i] ** 2) / (16 * p[i]) for i in range(len(v)))
    p_value = sp.gammainc((3 / 2), (Xi_kv / 2))
    return p_value

def main():
    """
    """
    