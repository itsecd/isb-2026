import sqlite3

class Database:
    def __init__(self, db_path="database.db"):
        """
        Initializes the Database instance and triggers table creation.

        Args:
            db_path (str): File system path for the SQLite database. Defaults to "database.db".

        Raises:
            TypeError: If the provided db_path is not a string.
        """

        if not isinstance(db_path, str):
            raise TypeError("Database path mist be a string.")
        self.db_path = db_path
        self.init_db()

    
    def connection(self):
        """
        Creates and returns a new connection object to the SQLite database.

        Returns:
            sqlite3.Connection: Active database connection descriptor.

        Raises:
            sqlite3.OperationalError: If the database file cannot be opened or accessed.
        """

        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.OperationalError as e:
            raise sqlite3.OperationalError(f"Failed to connect to database at {self.db_path}: {e}")
    

    def init_db(self):
        """
        Creates the 'users' table if it does not already exist within the schema.

        Ensures that necessary columns (id, username, password_hash, salt, is_safe) 
        are correctly configured with constraints. Guaranteed to close connection.

        Raises:
            sqlite3.Error: If any internal SQLite execution or commit fails.
        """

        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT,
                    is_safe INTEGER NOT NULL
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Database schema initialization failed: {e}")
        finally:
            conn.close()


    def add_user(self, username, password_hash, salt, is_safe):
        """
        Inserts a new user record atomically inside the database.

        Args:
            username (str): Unique identifier/login of the user.
            password_hash (str): Processed or hashed representation of the password.
            salt (Optional[str]): Hexadecimal salt string or None if unsafe mode is used.
            is_safe (bool): Flag indicating if secure hashing was enforced.

        Raises:
            TypeError: If arguments do not match expected types.
            sqlite3.IntegrityError: If the username already exists due to UNIQUE constraint.
            sqlite3.Error: For generic SQLite database execution failures.
        """

        if not isinstance(username, str) or not isinstance(password_hash, str):
            raise TypeError("Username and password hash must be strings.")
        if salt is not None and not isinstance(salt, str):
            raise TypeError("Salt must be a string or None.")
        if not isinstance(is_safe, bool):
            raise TypeError("is_safe parameter must be a boolean value.")
        
        conn = self.connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt, is_safe) VALUES (?, ?, ?, ?)",
                    (username, password_hash, salt, int(is_safe))
                )
        except sqlite3.IntegrityError as e:
            raise sqlite3.IntegrityError(f"User registration rejected. Username '{username}' already exists: {e}")
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to insert user record: {e}")
        finally:
            conn.close()


    def fetch_user(self, username):
        """
        Retrieves user authentication parameters matching the given username.

        Args:
            username (str): The login identifier to query.

        Returns:
            Optional[Tuple[str, Optional[str], int]]: A tuple containing 
            (password_hash, salt, is_safe) if found, otherwise None.

        Raises:
            TypeError: If the provided username is not a string.
            sqlite3.Error: If the database query execution fails.
        """

        if not isinstance(username, str):
            raise TypeError("Username query must be a string.")
        
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt, is_safe FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error querying user data for '{username}': {e}")
        finally:
            conn.close()
        
    
    def close(self):
        """
        Explicitly placeholder method to handle backward compatibility with Auth resource cleanup.
        """
        
        pass