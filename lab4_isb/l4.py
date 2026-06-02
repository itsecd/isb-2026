import random
import string
import hashlib
import csv
from tqdm import tqdm


def generate_random_string(length: int) -> str:
    """
    Генерация случайной строки из латинских букв и цифр.
    :param length: длина генерируемой строки
    :return: случайная строка заданной длины
    """

    if length <= 0:
        raise ValueError("Length must be a positive number")
    alphabet = string.ascii_letters + string.digits
    result = ''
    for _ in range(length):
        result += random.choice(alphabet)
    return result


def read_csv(filename: str) -> list[dict]:
    """
    Чтение данных из CSV-файла.
    :param filename: путь к CSV-файлу
    :return: список словарей, где каждый словарь соответствует одной строке CSV-файла
    """

    data = []
    try:
        with open(filename, 'r', encoding="utf-8", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except IsADirectoryError as e:
        raise IsADirectoryError(f"Expected CSV file path, got directory: {filename}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"CSV file not found: {filename}") from e
    except PermissionError as e:
        raise PermissionError(f"No permission to read CSV file: {filename}") from e
    except OSError as e:
        raise OSError(f"Error occurred while reading CSV file {filename}: {e}") from e
    return data


def create_dict_csv(filename: str, fieldnames: list) -> None:
    """
    Создание CSV-файла с заголовками для записи словарей.
    :param filename: путь к создаваемому CSV-файлу
    :param fieldnames: список названий столбцов CSV-файла
    :return: не возвращается
    """

    try:
        with open(filename, 'w', encoding="utf-8", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    except PermissionError as e:
        raise PermissionError(f"No permission to create CSV file: {filename}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Directory for CSV file does not exist: {filename}") from e
    except IsADirectoryError as e:
        raise IsADirectoryError(f"Expected CSV file path, got directory: {filename}") from e
    except OSError as e:
        raise OSError(f"Error occurred while creating CSV file {filename}: {e}") from e


def append_to_csv(filename: str, data: dict, fieldnames: list) -> None:
    """
    Добавление строки данных в CSV-файл.
    :param filename: путь к CSV-файлу
    :param data: словарь с данными для записи
    :param fieldnames: список названий столбцов CSV-файла
    :return: не возвращается
    """

    try:
        with open(filename, 'a', encoding="utf-8", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(data)
    except PermissionError as e:
        raise PermissionError(f"No permission to write to CSV file: {filename}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"CSV file path not found: {filename}") from e
    except ValueError as e:
        raise ValueError(f"Invalid CSV row format for {filename}. ""Data keys must match CSV fieldnames.") from e
    except OSError as e:
        raise OSError(f"Error occurred while writing to CSV file {filename}: {e}") from e


def stats_to_csv(filename: str, stats: list[dict]) -> None:
    """
    Сохранение статистики экспериментов в CSV-файл.
    :param filename: путь к CSV-файлу для сохранения статистики
    :param stats: список словарей со статистикой по длинам хеша
    :return: не возвращается
    """
    
    fieldnames = ["bits", "experiments", "average_attempts", "min_attempts", "max_attempts", "theory_attempts"]
    create_dict_csv(filename, fieldnames)
    for stat in stats:
        append_to_csv(filename, stat, fieldnames)


def hash_string (string: str) -> str:
    """
    Вычисление хеша строки.
    :param string: исходная строка для хеширования
    :return: SHA-256 хеш в шестнадцатеричном виде
    """

    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def cut_hash(hashed_string: str, bits: int) -> str:
    """
    Укорочение hex-представления хеша до заданного количества бит.
    :param hashed_string: полный хеш в шестнадцатеричном виде
    :param bits: длина укороченного хеша в битах, допустимые значения: 8, 12 или 16
    :return: укороченный хеш в шестнадцатеричном виде
    """

    if bits not in [8,12,16]:
        raise ValueError("Bits must be one of the following: 8, 12, 16")
    return hashed_string[:bits//4]


def find_collision(length: int, bits: int) -> dict:
    """
    Поиск первой коллизии для укороченного хеша.
    :param length: длина генерируемых случайных строк
    :param bits: длина укороченного хеша в битах, допустимые значения: 8, 12 или 16
    :return: словарь с найденной коллизией, строками и количеством попыток
    """

    hash_dict = {}
    attempts = 0
    while True:
        attempts += 1
        random_string = generate_random_string(length)
        random_hash = hash_string(random_string)
        cut_random_hash = cut_hash(random_hash, bits)
        if cut_random_hash in hash_dict:
            str1 = hash_dict[cut_random_hash]
            if str1 != random_string:
                return {
                    "hash": cut_random_hash,
                    "string1": str1,
                    "string2": random_string,
                    "attempts": attempts
                }
        hash_dict[cut_random_hash] = random_string


def experiment(length: int, bits: int, num_experiments: int, file_name: str) -> None:
    """
    Проведение серии экспериментов по поиску коллизий для выбранной длины хеша.
    :param length: длина генерируемых случайных строк
    :param bits: длина укороченного хеша в битах
    :param num_experiments: количество экспериментов
    :param file_name: путь к CSV-файлу для сохранения результатов экспериментов
    :return: не возвращается
    """

    if num_experiments <= 0:
        raise ValueError("Number of experiments must be a positive number")
    last_result = None
    print(f"Starting experiment with length={length}, bits={bits}, num_experiments={num_experiments}\n")
    for experiment_num in tqdm(range(1, num_experiments+1), desc="Experiments"):
        result = find_collision(length, bits)
        result["experiment"] = experiment_num
        result["bits"] = bits
        append_to_csv(file_name, result, fieldnames=["experiment", "bits", "hash", "string1", "string2", "attempts"])
        last_result = result
    print(
    f"Last collision: hash={last_result['hash']}, "
    f"attempts={last_result['attempts']}. ")
    print(f"Experiment with length={length}, bits={bits} completed and results saved to {file_name}")


def stats_from_csv(filename: str) -> list:
    """
    Подсчёт статистики по результатам экспериментов из CSV-файла.
    :param filename: путь к CSV-файлу с результатами поиска коллизий
    :return: список словарей со статистикой для каждой длины укороченного хеша
    """

    data = read_csv(filename)
    attempts_by_bits = {}
    for row in data:
        bits = int(row["bits"])
        attempts = int(row["attempts"])
        if bits not in attempts_by_bits:
            attempts_by_bits[bits] = []
        attempts_by_bits[bits].append(attempts)
    stats = []
    for bits, attempts_list in attempts_by_bits.items():
        experiments = len(attempts_list)
        average_attempts = sum(attempts_list) / experiments
        min_attempts = min(attempts_list)
        max_attempts = max(attempts_list)
        theory_attempts = 2 ** (bits / 2)
        stats.append({
            "bits": bits,
            "experiments": experiments,
            "average_attempts": average_attempts,
            "min_attempts": min_attempts,
            "max_attempts": max_attempts,
            "theory_attempts": theory_attempts
        })
    return stats



