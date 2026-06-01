from tqdm import tqdm
import hashlib
import hasher


DICTIONARY = ["password", "qwerty", "12345", "admin", "qwertyiop"]

def vuln_analyse(target_password: str) -> bool:
    """
    Анализ SHA-256 без соли
    Принимает: Пароль
    Возвращает: Данные о подборе пароля
    """
    print(f"\n[Анализ без соли] Целевой пароль: {target_password}")
    target_hash = hasher.hash_simple(target_password)["hash"]

    for guess in tqdm(DICTIONARY, desc="Перебор (Без соли)"):
        guess_hash = hashlib.sha256(guess.encode('utf-8')).hexdigest()
        if guess_hash == target_hash:
            print(f"Пароль успешно подобран: {guess}")
            return True
            
    print("Пароль не найден в словаре.")
    return False

def vuln_salt_analyse(target_password: str) -> bool:
    """
    Анализ SHA-256 с солью
    Принимает: Пароль (утёкший хэш)
    Возвращает: Статус о подборе пароля
    """
    print(f"Целевой пароль: {target_password}")

    leaked_record = hasher.hash_salted(target_password)
    target_hash = leaked_record["hash"]
    
    print(f"Утекший хэш: {target_hash}")

    for guess in tqdm(DICTIONARY, desc="Перебор"):
        guess_hash = hashlib.sha256(guess.encode('utf-8')).hexdigest()
        
        if guess_hash == target_hash:
            print(f"Пароль успешно подобран: {guess}")
            return True
            
    print("Пароль не удалось подобрать")
    return False
