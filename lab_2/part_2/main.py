import math

from scipy.special import gammaincc

from const import P_VALUE, PI, FILE, OUTPUT_FILE

def freq_test(seq: str) -> float:
    """frecuency test"""
    s_n = (seq.count('1')-seq.count('0'))/math.sqrt(len(seq))
    p_value = math.erfc(s_n / math.sqrt(2))
    return p_value

def replay_test(seq: str) -> float:
    """reply sequence test"""
    one_freq = seq.count('1')/len(seq)
    if not abs(one_freq- 0.5) < (2/math.sqrt(len(seq))):
        p_value = 0.0
    else:
        v_n = 0.0
        for i in range(0,len(seq)-1):
            if seq[i] != seq[i+1]:
                v_n+=1
        p_value =  math.erfc(abs(v_n - \
        2*len(seq)*one_freq*(1-one_freq))\
        / (2*math.sqrt(2*len(seq))*one_freq*(1-one_freq)))
    return p_value

def max_len_test(seq: str) -> float:
    """max len sequence if 1 test"""
    v = [0,0,0,0]
    for i in range(0,128,8):
        chank = seq[i:i + 8]
        one_count = max(len(s) for s in chank.split("0"))
        if one_count <= 1:
            v[0] += 1
        elif one_count == 2:
            v[1] += 1
        elif one_count == 3:
            v[2] += 1
        else:
            v[3] += 1
    x_2 = 0.0
    for i in range(0,4):
        x_2 += math.pow((v[i] - 16*PI[i]), 2) / (16 * PI[i])
    p_value = gammaincc(3 / 2, x_2 / 2)
    return p_value

def read_text(filename: str) -> str:
    """ function for read from file """
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found")
        exit(2)
    except PermissionError:
        print(f"Premision denied")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)

def main() -> None:
    seq_c = read_text(FILE[0])
    seq_j = read_text(FILE[1])
    seq_p = read_text(FILE[2])
    c_values = [
        "CPP",
        freq_test(seq_c),
        replay_test(seq_c),
        max_len_test(seq_c),
    ]
    j_values = [
        "JAVA",
        freq_test(seq_j),
        replay_test(seq_j),
        max_len_test(seq_j),
    ]
    p_values = [
        "PYTHON",
        freq_test(seq_p),
        replay_test(seq_p),
        max_len_test(seq_p),
    ]
    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write("Lang:   |  Freq Test  |  Same Test  | Max count Test | Result \n")
            f.write(
                f"{c_values[0]:<8}|  {c_values[1]:.7f}  |  {c_values[2]:.7f}  | {c_values[3]:.12f} | {"PASSED" if all(x >= P_VALUE for x in c_values[1:]) else "FAILED"}\n"
            )
            f.write(
                f"{j_values[0]:<8}|  {j_values[1]:.7f}  |  {j_values[2]:.7f}  | {j_values[3]:.12f} | {"PASSED" if all(x >= P_VALUE for x in j_values[1:]) else "FAILED"}\n"
            )
            f.write(
                f"{p_values[0]:<8}|  {p_values[1]:.7f}  |  {p_values[2]:.7f}  | {p_values[3]:.12f} | {"PASSED" if all(x >= P_VALUE for x in p_values[1:]) else "FAILED"}\n"
            )
    except Exception as e:
        print(f"Error: {e}\n")

if __name__ == "__main__":
    main()


        