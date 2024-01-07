import sqlite3

'''
abstract class
'''

class abstractSQL:
    def __init__(self, dbfile: str = "database.db"):
        """
        Initialize a DatabaseManager with the specified SQLite database file.

        Parameters:
        - dbfile (str): The path to the SQLite database file.
        """
        self.dbfile = dbfile
        self.connection = sqlite3.connect(self.dbfile)
        self.cursor = self.connection.cursor()
        
    
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