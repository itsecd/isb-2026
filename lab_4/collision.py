import itertools
from tqdm import tqdm
import create

def find_collision(secret_key: str, difficulty: int = 5) -> tuple[str, str, str]:
    """
    Ищет коллизию для усеченной части HMAC методом полного перебора.

    Args:
        secret_key (str): Секретный ключ аутентификации.
        difficulty (int): Количество начальных символов хэша для сравнения.
    """
    if not secret_key:
        raise ValueError("Секретный ключ не может быть пустым.")
        
    seen_hashes = {}
    
    with tqdm(desc="Поиск коллизии", unit=" шагов") as pbar:
        for i in itertools.count(1):
            text = f"сообщение_номер_{i}"
            full_hmac = create.create(text, secret_key)
            truncated_hmac = full_hmac[:difficulty]
            
            if truncated_hmac in seen_hashes:
                if seen_hashes[truncated_hmac] != text:
                    return seen_hashes[truncated_hmac], text, truncated_hmac
            
            seen_hashes[truncated_hmac] = text
            pbar.update(1)