from filereading import read_sequence
from seq_analyze import print_statistics, write_statistics


cpp_vect = read_sequence('generators/cpp/CppGen.txt')
print_statistics(cpp_vect, 'C++')
write_statistics(cpp_vect, 'C++')

java_vect = read_sequence('generators/java/JavaGenerated.txt')
print_statistics(java_vect, 'Java')
write_statistics(java_vect, 'Java')

python_vect = read_sequence('generators/python/PyGen.txt')
print_statistics(python_vect, 'Python')
write_statistics(python_vect, 'Python')
