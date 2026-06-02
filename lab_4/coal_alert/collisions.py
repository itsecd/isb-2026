import hash
import utils
import math
from tqdm import tqdm

def find_collision(hash_len: int, str_len: int) -> tuple[str, str, int, int]:
    """
    Функция для поиска первой коллизии для заданных длин случайной строки и укороченного хэша
    Принимает:
        hash_len - длина укороченного хэша
        str_len - длина случайной строки
    Возвращает:
        - кортеж [строка1, строка2, их одинаковый укороченный хэш, номер попытки, на которой произошла коллизия]
    """
    try:
        seen = {}
        max_attempts = (2 ** hash_len) + 1
        
        for attempt in tqdm(range(1, max_attempts + 1), desc=f"{hash_len} бит", unit="строка"):
            s = utils.generate_random_string(str_len)
            h = hash.find_shortened_hash(hash.find_hash_sha256(s), hash_len)
            
            if h in seen:
                if seen[h] != s:
                    return seen[h], s, h, attempt
            else:
                seen[h] = s
        return None
    except Exception as e:
        print(f"Сбой при поиске коллизии для {hash_len} бит: {e}")
        raise

def run_experiments(bits_list: tuple[int], experiments: int, str_len: int) -> dict:
    """
    Проведение серии экспериментов, сравнение с теорией и сбор метрик
    Принимает:
        bits_list - кортеж со значениями длины укороченного хэша
        experiments - кол-во экспериментов
        str_len - длина генерируемой случайной строки
    Возвращает:
        - словарь {"avg_attempts": среднее кол-во попыток на нахождение коллизии,
                    "theoretical": теоритическое кол-во попыток на нахождение коллизии}
    """
    print(f"Запуск {experiments} экспериментов\n")
    results = {}
    
    try:
        for bits in bits_list:
            total_attempts = 0
            successful_experiments = 0
            
            print(f"Тестирование для {bits} бит:")
            
            for i in range(experiments):
                res = find_collision(bits, str_len)
                if res:
                    attempts = res[-1]
                    total_attempts += attempts
                    successful_experiments += 1
            
            if successful_experiments == 0:
                print(f"[{bits} бит] коллизий нет(")
                continue
                
            avg_attempts = total_attempts / successful_experiments
            theoretical = math.sqrt(math.pi * (2 ** bits) / 2)
            
            print(f"    Среднее кол-во попыток (практика): {avg_attempts:.2f}")
            print(f"    Ожидаемое кол-во попыток (теория): {theoretical:.2f}")
            
            results[bits] = {"avg_attempts": avg_attempts, "theoretical": theoretical}
        return results
    except Exception as e:
        print(f"Ошибка при проведении серии экспериментов: {e}")
        raise