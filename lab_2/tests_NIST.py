import math
from const import CONST_PI, FILE
from scipy.special import erfc, gammaincc

def read_text(filename: str)->str:
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found")
        exit(2)
    except PermissionError:
        print(f"File not found")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)

def frequency_test(bits):
    n = len(bits)
    x = [1 if bit=='1' else -1 for bit in bits]
    s_n = abs(sum(x))/math.sqrt(n)

    pValue = erfc(s_n/math.sqrt(2))

    return pValue, pValue >= 0.01

def runs_test(bits):
    n = len(bits)
    psi=sum(1 for bit in bits if bit == '1')/n

    if abs(psi-0.5)>=2.0/math.sqrt(n):
        return 0.0, False
    
    v_n = 0
    for i in range(n-1):
        if bits[i]!=bits[i+1]:
            v_n+=1

    numerator = abs(v_n - 2 * n * psi * (1 - psi))
    denominator = 2*math.sqrt(2*n)*psi*(1-psi)

    if denominator == 0:
        return 0.0, False
    
    pValue=erfc(numerator/denominator)

    return pValue, pValue >=0.01

def long_run_test(bits):
    n = len(bits)

    if n!=128:
        raise ValueError("This test requires exactly 128 bits")

    m = 8
    v = [0,0,0,0]

    for i in range(16):
        block = bits[i*m:(i+1)*m]

        maxRun = 0
        currentRun = 0

        for bit in block:
            if bit == '1':
                currentRun+=1
                maxRun=max(maxRun,currentRun)
            else:
                currentRun = 0
        
        if maxRun <=1:
            v[0] += 1
        elif maxRun == 2:
            v[1]+=1
        elif maxRun == 3:
            v[2] +=1
        else:
            v[3]+=1

    chiSquared = 0
    for i in range(4):
        excepted = 16*CONST_PI[i]
        chiSquared+=((v[i]-excepted)**2)/excepted

    pValue = gammaincc(3/2, chiSquared/2)

    return pValue, pValue>=0.01


def main():
    seq_cpp = read_text(FILE[0])
    seq_python = read_text(FILE[1])
    seq_java = read_text(FILE[2])

    results = {
        'C++': (frequency_test(seq_cpp), runs_test(seq_cpp), long_run_test(seq_cpp)),
        'Java': (frequency_test(seq_java), runs_test(seq_java), long_run_test(seq_java)),
        'Python': (frequency_test(seq_python), runs_test(seq_python), long_run_test(seq_python))
    }    
    with open("result.txt", "w", encoding="utf-8") as f:
            
            f.write(f"{'Language':<8} | {'Frequency Test':<21} | {'Runs Test':<21} | {'Longest Run Test':<21}\n")
            f.write("-" * 80 + "\n")

            for lang, (freq, runs, long_run) in results.items():
                freq_p, freq_pass = freq
                runs_p, runs_pass = runs
                long_p, long_pass = long_run

                f.write(f"{lang:<8} | ")
                f.write(f"Freq: {freq_p:.6f} ({'PASS' if freq_pass else 'FAIL'}) | ")
                f.write(f"Runs: {runs_p:.6f} ({'PASS' if runs_pass else 'FAIL'}) | ")
                f.write(f"Long: {long_p:.6f} ({'PASS' if long_pass else 'FAIL'})\n")

    
    print("Results saved to result.txt")

if __name__ == "__main__":
    main()