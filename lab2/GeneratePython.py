import random

print("Python Generated Sequence (128 bits):")
sequence = ''.join(str(random.randint(0, 1)) for _ in range(128))
print(sequence)
