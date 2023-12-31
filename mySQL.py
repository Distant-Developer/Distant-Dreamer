import sqlite3

class dataSQL:
    def __init__(self, dbfile):
        """
        Initialize a DatabaseManager with the specified SQLite database file.

        Parameters:
        - dbfile (str): The path to the SQLite database file.
        """
        self.dbfile = dbfile
        self.connection = sqlite3.connect(self.dbfile)
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                token TEXT UNIQUE,
                username TEXT,
                email TEXT
            );
        ''')

        #id -> Unique Github ID
        #token -> todo()!
        #username -> User's Username
        #email -> Email Associated with Github