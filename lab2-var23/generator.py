import random

def run_generator():
    random.seed(24)

    binary_data = ''.join(
        str(random.randrange(2))
        for _ in range(128)
    )

    with open('gen_python.txt', 'w', encoding='utf-8') as file:
        file.write(binary_data)

    print("Данные успешно сохранены в файл gen_python.txt")

if __name__ == "__main__":
    run_generator()