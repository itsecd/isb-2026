import random

sequence = ''.join(str(random.randint(0, 1)) for _ in range(128))
print("Сгенерированная последовательность (Python):")
print(sequence)


with open("sequence_py.txt", "w") as f:
    f.write(sequence)