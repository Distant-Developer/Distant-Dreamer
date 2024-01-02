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
                "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                "token"	TEXT UNIQUE,
                "username"	TEXT DEFAULT NULL,
                "email"	INTEGER,
                "is_staff"	INTEGER NOT NULL DEFAULT 0,
                "linkedin_url" TEXT DEFAULT NULL,
                "github_url" TEXT DEFAULT NULL
            );
                                  
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER
            );
                                  
            CREATE TABLE IF NOT EXISTS "experiences" (
                "id"	INTEGER,
                "associated_user_id"	INTEGER NOT NULL,
                "company_name"	TEXT NOT NULL,
                "company_logo_url"	TEXT NOT NULL,
                "position_title"	TEXT NOT NULL,
                "position_description"	TEXT,
                "dates" TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );''')
        
        # users
        # id -> unique id (each user assigned one)
        # token -> user's github id or OAUTH token (should be unique)
        # username -> user's github name
        # email -> user's github email

        # posts
        # id -> unique id (each post assigned one)
        # owner_id -> unique id of user
        # TODO! 

        # experiences - (CONNECTED TO USERS EXPERIENCE)
        # id -> Each experience unique id
        # associated_user_id -> FOREIGN KEY OF user "id"
        # company_name -> Name of Company
        # company_logo_url -> URL of Company
        # position_title -> Position Title
        # position_description -> Position Description (Optionally Null)
        # dates -> Date of work
    
    def execute_script(self, target):
        self.cursor.executescript(f'''{target}''')

    def connect(self) -> sqlite3.Connection:
        """
        Establish a connection to the SQLite database.

        Returns:
        - sqlite3.Connection: A database connection object.
        """
        return sqlite3.connect(self.dbfile)

    def close(self):
        """Commit any pending changes and close the database connection."""
        self.connection.commit()
        self.connection.close()

    

    def get_count(self, target):
        self.connection = sqlite3.connect(self.dbfile)
        self.cursor = self.connection.cursor()


        self.cursor.execute("SELECT COUNT(*) FROM users WHERE token = ?", (target,))
        count = self.cursor.fetchone()[0]
        

        self.close()
        return count
    
    def user_exists(self, token):
        count = self.get_count(token)
        return int(count) >= 1


    def use_database(self, query: str, values: tuple = None, easySelect:bool=True):
        """
        Execute a database query and return the result.

        Parameters:
        - query (str): The SQL query to execute.
        - values (tuple, optional): A tuple of parameter values to bind to the query.

        Returns:
        - result: The result of the query execution. If it's a SELECT query, it returns the first row as a tuple; otherwise, it returns None.
        """
        self.connection = self.connect()

        res = self.connection.execute(query, values)
        returned_value = None
        if "select" in query.lower() and easySelect:
            returned_value = res.fetchone()
        else:
            returned_value = res.fetchall()

        self.close()
        return returned_value
    
    def get_experiences(self, users_id):
        list = self.use_database(
            "SELECT * from experiences where associated_user_id = ?", (users_id,), easySelect=False
        )
        return list