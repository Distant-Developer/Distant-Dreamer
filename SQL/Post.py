from SQL.abstractSQL import abstractSQL

class Post(abstractSQL):
    def __init__(self, id, owner_id, title, content, hidden):
        super().__init__("database.db")
        self.id = id
        self.owner_id = owner_id
        self.title = title
        self.content = content
        self.hidden = self.int_to_bool(hidden)

        self.owner_user = self.get_owner()
    
    def get_owner(self):
        from SQL.User import User
        raw = self.use_database(
            f"SELECT * FROM users where ID = {self.owner_id}", (), easySelect=False
        )

        return [User(*row) for row in raw][0]

    def get_comments(self):
        from SQL.Comment import Comment
        raw = self.use_database(
            f"SELECT * FROM comments where post_owner_id = {self.id}", (), easySelect=False
        )

        return [Comment(*row) for row in raw] #there can be several
    
    def get_three_comments(self):
        from SQL.Comment import Comment
        raw = self.use_database(
            f"SELECT * FROM comments where post_owner_id = {self.id}", (), easySelect=False
        )

        comments = [Comment(*row) for row in raw]
        return comments[:3], len(comments) > 3
    
    def delete(self):
        #delete all comments 
        #comments = self.get_comments() 
        #for comment in comments:
        #    self.use_database(
        #        "DELETE comments where id = ?;" (comment.id)
        #    )
        pass #TODO!

    def hide(self):
        self.use_database(
            f"UPDATE posts SET hidden = 1 WHERE id = ?", (self.id,)
        )
    
    def not_hidden(self): return not self.hidden