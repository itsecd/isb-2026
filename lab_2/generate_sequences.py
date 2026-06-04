import random
import secrets
import os

os.makedirs("generators/sequences", exist_ok=True)

LEN = 1_000_000

with open("generators/sequences/sequence_c.txt", "w") as f:
    for _ in range(LEN):
        f.write(str(random.getrandbits(1)))

rng = random.Random()
with open("generators/sequences/sequence_cpp.txt", "w") as f:
    for _ in range(LEN):
        f.write(str(rng.getrandbits(1)))

with open("generators/sequences/sequence_python.txt", "w") as f:
    for _ in range(LEN):
        f.write(str(secrets.randbits(1)))

print("Все три последовательности сгенерированы.")