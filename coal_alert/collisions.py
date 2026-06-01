import hash
import utils
import math
from tqdm import tqdm

def find_collision(hash_len: int, str_len: int, disable_tqdm: bool = False) -> tuple[str, str, int, int] | None:
    try:
        seen = {}
        max_attempts = (2 ** hash_len) + 1
        
        for attempt in tqdm(range(1, max_attempts + 1), desc=f"{hash_len} бит", unit="строка", disable=disable_tqdm):
            s = utils.generate_random_string(str_len)
            h = hash.find_shortened_hash(hash.find_hash_sha256(s), hash_len)
            
            if h in seen:
                if seen[h] != s:
                    return seen[h], s, h, attempt
            else:
                seen[h] = s
        return None
    except Exception as e:
        raise RuntimeError(f"Сбой при поиске коллизии для {hash_len} бит") from e

def run_experiments(bits_list: list[int], experiments: int, str_len: int) -> dict:
    """
    Проведение серии экспериментов, сравнение с теорией и сбор метрик
    """
    print(f"\n--- Запуск экспериментов ({experiments} итераций) ---")
    results = {}
    
    try:
        for bits in bits_list:
            total_attempts = 0
            successful_experiments = 0
            example_collision = None
            
            print(f"\nТестирование для {bits} бит:")
            
            for i in range(experiments):
                res = find_collision(bits, str_len, disable_tqdm=(experiments > 10))
                if res:
                    attempts = res[-1]
                    total_attempts += attempts
                    successful_experiments += 1
            
            if successful_experiments == 0:
                print(f"[{bits} бит] Коллизии не найдены.")
                continue
                
            avg_attempts = total_attempts / successful_experiments
            theoretical = math.sqrt(math.pi * (2 ** bits) / 2)
            
            print(f"    Среднее кол-во попыток (практика): {avg_attempts:.2f}")
            print(f"    Ожидаемое кол-во попыток (теория): {theoretical:.2f}")
            
            results[bits] = {"avg_practice": avg_attempts, "theory": theoretical, "example": example_collision}
        return results
    except Exception as e:
        raise RuntimeError("Ошибка при проведении серии экспериментов") from e