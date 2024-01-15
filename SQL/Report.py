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
        elif self.target_type=="jobPost":
            x = self.get_original_Jobpost()
            return detailedReport(x.owner_id, x.position_content)
        
    def hide_content(self):
        if self.target_type == "post":
            x = self.get_original_post()
            x.hide()
        elif self.target_type == "jobPost":
            x = self.get_original_Jobpost()
            x.hide()

    
    def get_original_post(self):
        from SQL.Post import Post
        raw = self.use_database(
            f"SELECT * FROM posts where ID = {self.target_id}", (), easySelect=False
        )

        return [Post(*row) for row in raw][0] #there should be only one lol
    
    def get_original_Jobpost(self):
        from SQL.JobPost import JobPost
        raw = self.use_database(
            f"SELECT * FROM Jobpost where ID = {self.target_id}", (), easySelect=False
        )

        return [JobPost(*row) for row in raw][0] #there should be only one lol
    
    def not_archived(self):
        return not self.archived
    
    def owner_is_organization(self):
        """
        Checks if we are sending a report on an user/organization who caused said incident
        """
        return self.target_type == "jobPost"
    
    def get_org_owner(self):
        from SQL.Organization import Organization
        raw = self.use_database(
            f"SELECT * FROM organizations where ID = {self.owner_id}", (), easySelect=False
        )

        return [Organization(*row) for row in raw][0] #should return 1 org; each post MUST have an owner
    
class detailedReport():
    def __init__(self, owner_user, content):
        self.owner_user = owner_user
        self.content = content