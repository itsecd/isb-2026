import random
import string
from tqdm import tqdm
import auth          
import auth_no_salt 

def run_collision_brute(username: str, data: dict):
    """
    Функция случайного подбора коллизии с визуализацией через tqdm
    """
    stored_hash = data.get(username)
    if not stored_hash:
        print(f"Пользователь {username} не найден для подбора коллизии.")
        return

    if not isinstance(stored_hash, str):
        print(f"Ошибка: Данные хэша для {username} повреждены или имеют неверный формат.")
        return

    # Определяем, какой хэш перед нами. SHA-256 всегда имеет длину 64 символа.
    is_no_salt = len(stored_hash) == 64

    if is_no_salt:
        print(f"Запуск случайного подбора коллизии (БЕЗ СОЛИ) для пользователя {username}...")
        max_attempts = 10000 
    else:
        print(f"Запуск случайного подбора коллизии (С СОЛЬЮ) для пользователя {username}...")
        max_attempts = 50

    chars = string.ascii_lowercase + string.digits
    found_password = None
    
    try:
        with tqdm(total=max_attempts, desc="Подбор коллизии", unit=" попытка") as pbar:
            for _ in range(max_attempts):
                length = random.randint(4, 6)
                candidate = "".join(random.choice(chars) for _ in range(length))
                
                pbar.set_postfix(current=candidate)
                
                # Проверка совпадения в зависимости от режима хэша
                if is_no_salt:
                    if auth_no_salt.check_password_no_salt(candidate, stored_hash):
                        found_password = candidate
                        pbar.update(1)
                        break
                else:
                    if auth.check_password(candidate, stored_hash):
                        found_password = candidate
                        pbar.update(1)
                        break
                        
                pbar.update(1)
    except Exception as e:
        print(f"\nОшибка во время выполнения брутфорса: {e}")
        return
    
    if found_password:
        print(f"[УСПЕХ] Коллизия найдена случайным перебором: '{found_password}'")
    else:
        print(f"[FAIL] За {max_attempts} случайных генераций совпадений не найдено.")