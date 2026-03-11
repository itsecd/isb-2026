import random

with open("bits_python.txt", "w") as f:
    for _ in range(128):
        f.write(str(random.randint(0,1)))