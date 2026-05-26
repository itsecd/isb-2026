import time
from tqdm import tqdm
from hash_units import calculate_hash, generate_salt


RAINBOW_DICTIONARY = [
    "123456", "password", "qwerty", "admin", "123456789", 
    "letmein", "supersecret", "minialbina", "security", "unknown"
]


def run_attack_demo():
    target_password = "minialbina"
    print(f"[INFO] Target user's actual password: '{target_password}'\n")

    print("[CASE 1] Attacking UNSECURE storage (No Salt)")
    stolen_plain_hash = calculate_hash(target_password)
    print(f"[INPUT] Stolen Hash: {stolen_plain_hash}")
    
    found_password = None
    for word in tqdm(RAINBOW_DICTIONARY, desc="Brute-forcing plain hash", unit=" word"):
        time.sleep(0.3) 
        
        if calculate_hash(word) == stolen_plain_hash:
            found_password = word
            break
            
    if found_password:
        print(f"[SUCCESS] Password CRACKED! Result: '{found_password}'")
        print("[ANALYSIS] Vulnerability confirmed: Plain hashes are weak to rainbow tables.")
    else:
        print("[FAIL] Password not found in dictionary.")

    print("-" * 60)

    print("[CASE 2] Attacking SECURE storage (With Salt)")
    stolen_salt = generate_salt()
    stolen_salted_hash = calculate_hash(target_password, stolen_salt)
    print(f"[INPUT] Stolen Hash: {stolen_salted_hash}")
    print(f"[INPUT] Stolen Salt: {stolen_salt}")
    
    found_salted_password = None
    
    for word in tqdm(RAINBOW_DICTIONARY, desc="Brute-forcing salted hash", unit=" word"):
        time.sleep(0.3)
        
        if calculate_hash(word, stolen_salt) == stolen_salted_hash:
            found_salted_password = word
            break
            
    if found_salted_password:
        print(f"[SUCCESS] Password found: '{found_salted_password}'")
        print("[ANALYSIS] Even though the password was guessed, salt forces the attacker\n"
              "           to compute hashes for every single user INDIVIDUALLY.\n"
              "           Massive pre-computed Rainbow Tables are now completely USELESS!")
    else:
        print("[FAIL] Attack failed.")
        

if __name__ == "__main__":
    run_attack_demo()
