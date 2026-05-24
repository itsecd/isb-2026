import json
import secrets
import bcrypt
from tqdm import tqdm
from DB import Database


class Auth:
    def __init__(self, settings="settings.json", db_path=None):
        self.load_settings(settings)
        database_path = db_path if db_path else self.settings.get("db_path", "database.db")
        self.db = Database(database_path)


    def load_settings(self, settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {
                "db_path": "database.db",
                "use_salt": True,
                "salt_length": 16,
                "bruteforce_iters": 2000,
                "bcrypt_rounds": 12
            }
        

    def validate(self, username, password):
        if not username or not password:
            raise ValueError("Login and password cant be empty.")
        

    def generate_salt(self):
        length = self.settings.get("salt_length", 16)
        return secrets.token_hex(length)
    

    def unsafe_gen_hash(self, password):
        return password.encode('utf-8').hex()
    

    def safe_gen_hash(self, password, salt):
        salted_password = password + salt
        rounds = self.settings.get("bcrypt_rounds", 12)
        bcrypt_salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(salted_password.encode('utf-8'), bcrypt_salt)
        return hashed.decode('utf-8')
    

    def unsafe_registration(self, username, password):
        self.validate(username, password)
        hashed = self.unsafe_gen_hash(password)
        self.db.add_user(username, hashed, salt=None, is_safe=False)


    def safe_registration(self, username, password):
        self.validate(username, password)
        salt = self.generate_salt()
        hashed = self.safe_gen_hash(password, salt)
        self.db.add_user(username, hashed, salt=salt, is_safe=True)


    def check_unsafe_password(self, password, stored_hash):
        return self.unsafe_gen_hash(password) == stored_hash
    

    def check_safe_password(self, password, stored_hash, salt):
        salted_password = password + salt
        return bcrypt.checkpw(salted_password.encode('utf-8'), stored_hash.encode('utf-8'))
    

    def verify_user(self, username, password):
        userdata = self.db.fetch_user(username)
        if not userdata:
            return False
        stored_hash, salt, is_safe = userdata
        if is_safe:
            return self.check_safe_password(password, stored_hash, salt)
        return self.check_unsafe_password(password, stored_hash)
    

    def check_candidate(self, candidate, target_hash):
        return self.unsafe_gen_hash(candidate) == target_hash
    

    def check_collisions(self, target_hash):
        iters = self.settings.get("bruteforce_iters", 2000)
        for i in tqdm(range(iters)):
            candidate = str(i)
            if self.check_candidate(candidate, target_hash):
                return candidate
        return None
    

    def close(self):
        self.db.close()