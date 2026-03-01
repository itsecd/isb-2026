import subprocess
import os
import sys
import argparse
import math
from scipy import special as sc

def read_numbers(filename: str) -> list[int]:
    """
    Считывает числовую последовательность из файла
    """
    result = []
    try:
        with open(filename, encoding="utf-8") as file:
            for i in file.read():
               if i == "0" or i == "1":
                    result.append(int(i))
        return result
    except Exception as e:
        raise e
    

def run_cpp(run_file: str, count: int, output_file: str):
    """
    Запуск cpp файла
    """
    if not os.path.exists(run_file):
        raise FileNotFoundError(f"File {run_file} is not found")
    try:
        result = subprocess.run([run_file, str(count), output_file])
        if result.returncode != 0:
            raise RuntimeError(f"Error {result.returncode}")
    except Exception as e:
        raise RuntimeError(f"File {run_file} is not correct.")
    

def run_java(java_file: str, count: int, output_file: str):
    """
    Запуск java файла
    """
    if not os.path.exists(java_file):
        raise FileNotFoundError(f"File {java_file} is not found")
    
    java_dir = os.path.dirname(java_file)           
    parent_dir = os.path.dirname(java_dir)   
    folder_name = os.path.basename(java_dir)
    file_name = os.path.basename(java_file).replace('.java', '')
    
    class_name = f"{folder_name}.{file_name}"

    try:
        comp_result = subprocess.run(["javac", java_file])
        if comp_result.returncode != 0:
            raise RuntimeError(f"Compile error {comp_result.returncode}")
        
        run_result = subprocess.run(["java", "-cp", parent_dir, class_name, str(count), output_file])
        if run_result.returncode != 0:
            raise RuntimeError(f"Run error {run_result.returncode}")
        
    except Exception as e:
        raise RuntimeError(f"File {java_file} is not correct.")
    

def run_python(run_file: str, count: int, output_file: str):
    """
    Запуск py файла
    """
    if not os.path.exists(run_file):
        raise FileNotFoundError(f"File {run_file} is not found")
    try:
        result = subprocess.run([sys.executable, run_file, "--count", str(count), "--writefile", output_file])
        if result.returncode != 0:
            raise RuntimeError(f"Error {result.returncode}")
    except Exception as e:
        raise RuntimeError(f"File {run_file} is not correct.")


def NIST1(bits: list[int]) -> bool:
    """
    1 тест NIST
    """
    result = 0.0

    result = sum(1 if b == 1 else -1 for b in bits)
    result = result/math.sqrt(len(bits))
    
    result = math.erfc(result/math.sqrt(2))

    return result >= 0.01


def NIST2(bits: list[int]) -> bool:
    """
    2 тест NIST
    """
    j = 0.0

    j = sum(bits)/len(bits)
    if abs(j - 0.5) >= 2/math.sqrt(len(bits)):
        return False
    v = 0
    for i in range(len(bits)-1):
        if(bits[i] != bits[i+1]):
            v+=1
    result = abs(v-2*len(bits)*j*(1-j))/(2*math.sqrt(2*len(bits))*j*(1-j))
    result = math.erfc(result)
    return result >= 0.01

def NIST3(bits: list[int]) -> bool:
    """
    3 тест NIST
    """
    v = [0, 0, 0, 0]
    n = [0.2148, 0.3672, 0.2305, 0.1875]

    mini_bits = []
    
    for i in range(int(len(bits)/8)):
        mini_bits.append([])
        for j in range(8):
            mini_bits[i].append(bits[i*8 + j])

    for block in mini_bits:
        current_num = 0
        max_num = 0

        for i in block:
            if i == 1:
                current_num = current_num + 1
                max_num = max(max_num, current_num)
            else:
                current_num = 0

        if max_num <= 1:
            v[0] += 1
        if max_num == 2:
            v[1] += 1
        if max_num == 3:
            v[2] += 1
        if max_num >= 4:
            v[3] += 1

    x = 0
    for i in range(4):
        x = x + (v[i] - 16*n[i])**2/(16*n[i])

    result = sc.gammaincc(3/2, x/2)
    return result >= 0.01


def bool_to_str(f: bool)->str:
    """
    Преобразует bool в str
    """
    if f:
        return "success"
    else:
        return "failure"


def res_funk(cpp_file: str, java_file: str, py_file: str, res_file: str):
    """
    Записывает итоговый результат
    """
    try:
        with open(res_file, "w", encoding="utf-8") as file:
            file.write("Generator c++:\n")
            bits_cpp = read_numbers(cpp_file)
            file.write(f"Test1: {bool_to_str(NIST1(bits_cpp))}\n")
            file.write(f"Test2: {bool_to_str(NIST2(bits_cpp))}\n")
            file.write(f"Test3: {bool_to_str(NIST3(bits_cpp))}\n\n")

            file.write("Generator java:\n")
            bits_java = read_numbers(java_file)
            file.write(f"Test1: {bool_to_str(NIST1(bits_java))}\n")
            file.write(f"Test2: {bool_to_str(NIST2(bits_java))}\n")
            file.write(f"Test3: {bool_to_str(NIST3(bits_java))}\n\n")

            file.write("Generator python:\n")
            bits_py = read_numbers(py_file)
            file.write(f"Test1: {bool_to_str(NIST1(bits_py))}\n")
            file.write(f"Test2: {bool_to_str(NIST2(bits_py))}\n")
            file.write(f"Test3: {bool_to_str(NIST3(bits_py))}")
    except Exception as e:
        raise e


def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--count", "-c", default=128, type=int, help="число бит на выдачу.")

    parser.add_argument("--runfile_cpp", "-rc", default="build/Debug/generator.exe", type=str, help="Путь к файлу c++.")
    parser.add_argument("--runfile_java", "-rj", default="lab_2/generators/generator.java", type=str, help="Путь к файлу java.")
    parser.add_argument("--runfile_py", "-rp", default="lab_2/generators/generator.py", type=str, help="Путь к файл python.")

    parser.add_argument("--writefile_cpp", "-wc", default="lab_2/gen_bits/cpp_gen.txt", type=str, help="Путь к файлу для записи результата c++.")
    parser.add_argument("--writefile_java", "-wj", default="lab_2/gen_bits/java_gen.txt", type=str, help="Путь к файлу для записи результата java.")
    parser.add_argument("--writefile_py", "-wp", default="lab_2/gen_bits/python_gen.txt", type=str, help="Путь к файлу для записи результата python.")
    
    parser.add_argument("--resultfile", "-r", default="lab_2/result.txt", type=str, help="Путь к файлу для записи результата python.")
    args = parser.parse_args()

    try:
        run_cpp(args.runfile_cpp, args.count, args.writefile_cpp)
        run_java(args.runfile_java, args.count, args.writefile_java)
        run_python(args.runfile_py, args.count, args.writefile_py)
    except Exception as e:
        print(f"Error: {e}")
        raise e
    
    try:
        res_funk(args.writefile_cpp, args.writefile_java, args.writefile_py, args.resultfile)
    except Exception as e:
        print(f"Error: {e}")
        raise e


if __name__ == "__main__":
    main()