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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE,
                username TEXT,
                email TEXT,
            );
                                  
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
            );
        ''')
        
        # users
        # id -> unique id (each user assigned one)
        # token -> user's github id 
        # username -> user's github name
        # email -> user's github email

        # posts
        # id -> unique id (each post assigned one)
        # owner_id -> unique id of user
        # TODO! 