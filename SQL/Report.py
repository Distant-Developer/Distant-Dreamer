from SQL.abstractSQL import abstractSQL


class Report(abstractSQL):
    def __init__(self, id, owner_id, reason, target_id, target_type, archived, action, action_reason):
        super().__init__("database.db")
        self.id = id
        self.owner_id = owner_id
        self.reason = reason
        self.target_id = target_id
        self.target_type = target_type
        self.archived = self.int_to_bool(archived)
        self.action = action
        self.action_reason = action_reason

        self.detailed_report = self.get_content()

    def get_owner(self):
        from SQL.User import User
        raw = self.use_database(
            f"SELECT * FROM users where ID = {self.owner_id}", (), easySelect=False
        )

        return [User(*row) for row in raw][0]
    
    def get_content(self):
        if self.target_type=="post":
            x = self.get_original_post()
            return detailedReport(x.owner_id, x.content)
        
    def hide_content(self):
        if self.target_type == "post":
            x = self.get_original_post()
            x.hide()

    
    def get_original_post(self):
        from SQL.Post import Post
        raw = self.use_database(
            f"SELECT * FROM posts where ID = {self.target_id}", (), easySelect=False
        )

        return [Post(*row) for row in raw][0] #there should be only one lol
    
    def not_archived(self):
        return not self.archived
    
class detailedReport():
    def __init__(self, owner_user, content):
        self.owner_user = owner_user
        self.content = content