
from SQL.abstractSQL import abstractSQL


class Comment(abstractSQL):
    def __init__(self, id, owner_id, post_owner_id, content):
        super().__init__()
        self.id = id
        self.owner_id = owner_id
        self.post_owner_id = post_owner_id
        self.content = content

    
    def get_owner(self):
        from SQL.User import User
        raw = self.use_database(
            f"SELECT * FROM users where ID = {self.owner_id}", (), easySelect=False
        )

        return [User(*row) for row in raw][0] #there should be only one lol
    
    def get_original_post(self):
        from SQL.Post import Post
        raw = self.use_database(
            f"SELECT * FROM posts where ID = {self.post_owner_id}", (), easySelect=False
        )

        return [Post(*row) for row in raw][0] #there should be only one lol