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
    
    def get_organizations(self, id=None, owner_id=None):
        from SQL.Organization import Organization
        if target := id:
            raw = self.use_database(
                "SELECT * from organizations WHERE id = ?", (int(target),), easySelect=False
            )
        elif target := owner_id:
            raw = self.use_database(
                "SELECT * from organizations WHERE owner_id = ?", (int(target),), easySelect=False
            )
        else:
            raw = self.use_database(
                "SELECT * from organizations", (), easySelect=False
            )
        return [Organization(*row) for row in raw]
    
    def int_to_bool(self, input):
        if input == 0: 
            return False 
        elif input == 1:
            return True