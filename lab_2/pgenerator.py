import random

seq = ''
for _ in range(128):
    seq += str(random.randint(0, 1))

with open('sequence_python.txt', 'w') as f:
    f.write(seq)

print(seq)