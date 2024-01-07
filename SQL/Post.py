from SQL.abstractSQL import abstractSQL

class Post(abstractSQL):
    def __init__(self, id, owner_id, title, content):
        super().__init__("database.db")
        self.id = id
        self.owner_id = owner_id
        self.title = title
        self.content = content

        print(self.dbfile)

        self.owner_user = self.get_owner()

        
    
    def get_owner(self):
        from SQL.User import User
        raw = self.use_database(
            f"SELECT * FROM users where ID = {self.owner_id}", (), easySelect=False
        )

        return [User(*row) for row in raw][0]

