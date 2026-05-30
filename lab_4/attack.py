import math
from typing import Tuple, Optional, Dict, List
from tqdm import tqdm
from hash_utils import generate_random_string, get_hash

def find_collision(bits: int, max_attempts: int = 100000) -> Tuple[Optional[str], Optional[str], int, Dict[str, str]]:
    """Ищет коллизию хеша — две различные строки с одинаковым укороченным хешем.

    Args:
        bits: Длина укороченного хеша в битах (8, 12, 16).
        max_attempts: Максимальное количество генерируемых строк для поиска.

    Returns:
        Tuple[Optional[str], Optional[str], int, Dict[str, str]]: Кортеж, содержащий:
            - Первая строка с найденным хешом (или None).
            - Вторая строка с найденным хешом (или None).
            - Общее количество предпринятых попыток.
            - Таблица всех сгенерированных хешей и соответствующих им строк.
    """
    match bits in (8, 12, 16):
        case False:
            raise ValueError("Допустимые значения bits: 8, 12 или 16.")
        case True:
            pass

    hash_table: Dict[str, str] = {}
    attempts = 0

    try:
        with tqdm(total=max_attempts, desc=f"Поиск коллизии ({bits} бит)", unit="попыток", disable=False) as pbar:
            for _ in range(max_attempts):
                attempts += 1
                data = generate_random_string()
                hash_value = get_hash(data, bits)

                match hash_value in hash_table:
                    case True:
                        existing_data = hash_table[hash_value]
                        match existing_data != data:
                            case True:
                                pbar.update(1)
                                return existing_data, data, attempts, hash_table
                            case False:
                                pass  # Дубликат строки, пропускаем
                    case False:
                        pass

                hash_table[hash_value] = data
                pbar.update(1)

        return None, None, attempts, hash_table
    except KeyboardInterrupt:
        print("\nПоиск прерван пользователем.")
        return None, None, attempts, hash_table
    except Exception as e:
        raise RuntimeError(f"Критическая ошибка во время поиска коллизии: {e}") from e

def run_experiments(bits: int, experiments_count: int = 5, max_attempts: int = 100000) -> List[dict]:
    """Проводит серию независимых экспериментов по поиску коллизий.

    Args:
        bits: Длина укороченного хеша в битах.
        experiments_count: Количество запусков поиска коллизии.
        max_attempts: Лимит попыток для каждого эксперимента.

    Returns:
        List[dict]: Список словарей с результатами каждого эксперимента.
    """
    results = []
    for i in range(experiments_count):
        print(f"Эксперимент {i + 1}/{experiments_count} для {bits} бит...")
        try:
            str1, str2, attempts, _ = find_collision(bits, max_attempts)

            match (str1 is not None, str2 is not None):
                case (True, True):
                    results.append({
                        "bits": bits,
                        "experiment": i + 1,
                        "str1": str1,
                        "str2": str2,
                        "hash1": get_hash(str1, bits),
                        "hash2": get_hash(str2, bits),
                        "attempts": attempts,
                        "success": True
                    })
                case _:
                    results.append({
                        "bits": bits,
                        "experiment": i + 1,
                        "success": False,
                        "attempts": attempts
                    })
        except Exception as e:
            print(f"Ошибка в эксперименте {i + 1}: {e}")
            results.append({
                "bits": bits,
                "experiment": i + 1,
                "success": False,
                "attempts": 0,
                "error": str(e)
            })
    return results

def get_expected_attempts(bits: int) -> int:
    """Рассчитывает теоретическое ожидаемое количество попыток до возникновения коллизии.

    Args:
        bits: Длина хеша в битах.

    Returns:
        int: Округлённое до целого ожидаемое количество попыток.
    """
    match bits < 0:
        case True:
            raise ValueError("Длина хеша не может быть отрицательной.")
        case False:
            pass
    return int(math.sqrt(math.pi * (2 ** bits) / 2))