import random

def generate_sequence(length=128):
    return ''.join(random.choice('01') for _ in range(length))

# Пример использования
seq = generate_sequence(128)
with open('generated_sequence.txt', 'w') as f:
    f.write(seq)

print("Генерация завершена. Сохранено в generated_sequence.txt")