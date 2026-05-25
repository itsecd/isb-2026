import time
from tqdm import tqdm
from no_crack import hash_password_no_salt
from file_open_and_close import load_config, load_user_database

def run_collision_attack(config_path="settings.json"):
    """
    Демонстрирует уязвимость бессолевой схемы.
    Ищет совпадения хэшей по словарю популярных паролей с анимацией tqdm.
    """
    try:
        config = load_config(config_path)
        db_path = config.get("files", {}).get("data_base_no_salt", "data_base_no_salt.json")
        db = load_user_database(db_path)
        
        if not db:
            print("[-] Data base empty or not found. Register users first, damn it!")
            return

        # Популярные пароли для проверки коллизий/подбора
        common_passwords = ["123", "123456", "qwerty", "password", "admin", "ааа", "Alice", "Anapa2006"]
        
        print(f"\n[+] Launch collison analysys for {len(db)} users...")
        time.sleep(0.5)

        # Визуализация процесса через tqdm
        for password in tqdm(common_passwords, desc="Scannon password dictionary", unit="pwd"):
            # Вычисляем один хэш для пароля (ведь соли нет, он один на всех!)
            current_hash = hash_password_no_salt(password)
            matched_users = [user for user, data in db.items() if data.get("hash") == current_hash]
            
            if matched_users:
                tqdm.write(f"\n[Ahtung, collision found]: Password '{password}' can be used in accounts: {', '.join(matched_users)}")
                tqdm.write(f"-> Hash in data base: {current_hash}\n")
                
    except Exception as e:
        print(f"[-] Error in collision analysys module: {e}")