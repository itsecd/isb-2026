import json
import secrets
import bcrypt
from tqdm import tqdm
from DB import Database


class Auth:
    def __init__(self, settings="settings.json", db_path=None):
        """
        Constructs system subsystems and initializes underlying database linkage.

        Args:
            settings (str): File system path pointing to JSON settings. Defaults to "settings.json".
            db_path (Optional[str]): Explicit override database location path.

        Raises:
            TypeError: If configurations file parameters paths are not string types.
        """
        if not isinstance(settings, str):
            raise TypeError("Settings configuration file path must be a string.")
        if db_path is not None and not isinstance(db_path, str):
            raise TypeError("Override database path parameter must be a string.")
        
        self.load_settings(settings)
        database_path = db_path if db_path else self.settings.get("db_path", "database.db")
        self.db = Database(database_path)


    def load_settings(self, settings_path):
        """
        Reads system environment adjustments from a JSON document or falls back to standard limits.

        Args:
            settings_path (str): File system path to parse configuration from.
        """

        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
                if not isinstance(self.settings, dict):
                    raise ValueError("Configuration roots must be a dictionary object.")
                
        except (FileNotFoundError, json.JSONDecodeError, ValueError, PermissionError):
            self.settings = {
                "db_path": "database.db",
                "use_salt": True,
                "salt_length": 16,
                "bruteforce_iters": 2000,
                "bcrypt_rounds": 12
            }
        

    def validate(self, username, password):
        """
        Ensures credentials conform to primitive object structures and lengths constraints.

        Args:
            username (Any): Candidate login string object.
            password (Any): Candidate cleartext password object.

        Raises:
            TypeError: If input arguments are not explicit string representations.
            ValueError: If objects evaluate to empty spaces or contain blank structures.
        """

        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("Credentials parameters must be explicitly typed as strings.")
        if not username.strip() or not password.strip():
            raise ValueError("Login and password structures cannot be empty or whitespaces.")
        

    def generate_salt(self):
        """
        Assembles secure pseudorandom token hex blocks via high-entropy OS calls.

        Returns:
            str: Hexadecimal string representing high-entropy salt bits.

        Raises:
            ValueError: If configured configurations assign invalid length metrics.
        """

        length = self.settings.get("salt_length", 16)
        if not isinstance(length, int) or length <= 0:
            raise ValueError("Configured salt length parameters must be positive integers.")
        return secrets.token_hex(length)
    

    def unsafe_gen_hash(self, password):
        """
        Calculates low-overhead deterministic linear hex representations from strings.

        Args:
            password (str): Cleartext candidate data.

        Returns:
            str: Non-salted predictable hexadecimal string.
        """

        return password.encode('utf-8').hex()
    

    def safe_gen_hash(self, password, salt):
        """
        Computes computationally intensive keyspaces signatures via bcrypt workflows.

        Args:
            password (str): Target string element to wrap.
            salt (str): Cryptographic system application noise salt token.

        Returns:
            str: Safe hashed output incorporating bounds signatures.

        Raises:
            RuntimeError: Cryptographic failure within safe hash routines calculation.
        """

        salted_password = password + salt
        rounds = self.settings.get("bcrypt_rounds", 12)
        try:
            bcrypt_salt = bcrypt.gensalt(rounds=rounds)
            hashed = bcrypt.hashpw(salted_password.encode('utf-8'), bcrypt_salt)
            return hashed.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Cryptographic failure within safe hash routines calculation: {e}")
    

    def unsafe_registration(self, username, password):
        """
        Signs up a user without utilizing salts, mapping directly to vulnerability models.

        Args:
            username (str): Desired account unique user string.
            password (str): Intended verification key.
        """

        self.validate(username, password)
        hashed = self.unsafe_gen_hash(password)
        self.db.add_user(username, hashed, salt=None, is_safe=False)


    def safe_registration(self, username, password):
        """
        Protects accounts using unique entropy factors alongside variable iteration cost hashes.

        Args:
            username (str): Desired account unique user string.
            password (str): Intended validation token.
        """

        self.validate(username, password)
        salt = self.generate_salt()
        hashed = self.safe_gen_hash(password, salt)
        self.db.add_user(username, hashed, salt=salt, is_safe=True)


    def check_unsafe_password(self, password, stored_hash):
        """
        Performs clear validations of direct matching strings properties.

        Args:
            password (str): User authentication attempt cleartext payload.
            stored_hash (str): Target DB validation model matching sequence.

        Returns:
            bool: Verification success status flag.
        """

        return self.unsafe_gen_hash(password) == stored_hash
    

    def check_safe_password(self, password, stored_hash, salt):
        """
        Executes timing-attack safe evaluations on crypt hashes.

        Args:
            password (str): User authentication attempt cleartext payload.
            stored_hash (str): Multi-round signature retrieved from repository state.
            salt (str): Decoupled user isolation component salt sequence.

        Returns:
            bool: Authenticated true state or false misalignments flag.
        """

        salted_password = password + salt
        try:
            return bcrypt.checkpw(salted_password.encode('utf-8'), stored_hash.encode('utf-8'))
        except Exception:
            return False
    

    def verify_user(self, username, password):
        """
        Determines user authenticity by extracting data from the database.

        Args:
            username (str): Target login search criterion.
            password (str): Validation payload payload structure.

        Returns:
            bool: Validation feedback parameter.
        """

        if not isinstance(username, str) or not isinstance(password, str):
            return False
        try:
            userdata = self.db.fetch_user(username)
            if not userdata:
                return False
            stored_hash, salt, is_safe = userdata

            match is_safe:
                case 1:
                    return self.check_safe_password(password, stored_hash, salt)
                case 0:
                    return self.check_unsafe_password(password, stored_hash)
                case _:
                    return False
        except Exception:
            return False
    

    def check_candidate(self, candidate, target_hash):
        """
        Checks whether an incremental numerical search string aligns with an unsalted signature.

        Args:
            candidate (str): Current brute-force iteration sequence attempt.
            target_hash (str): Reference database record sequence payload.

        Returns:
            bool: True if alignment is confirmed, False otherwise.
        """

        return self.unsafe_gen_hash(candidate) == target_hash
    

    def bruteforce(self, target_hash):
        """
        Simulates iterative audit operations targeting un-salted linear structures keyspaces.

        Args:
            target_hash (str): Stolen flat representation hash to invert.

        Returns:
            Optional[str]: Original recovered plain text integer sequence if found, else None.
        """
        if not isinstance(target_hash, str):
            return None
        
        iters = self.settings.get("bruteforce_iters", 2000)
        if not isinstance(iters, int) or iters <= 0:
            iters = 2000

        for i in tqdm(range(iters)):
            candidate = str(i)
            if self.check_candidate(candidate, target_hash):
                return candidate
        return None
    

    def close(self):
        """
        Signals storage drivers to drop connections safely to preserve integrity.
        """

        self.db.close()