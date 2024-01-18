import json

from SQL.abstractSQL import abstractSQL

class Applicant(abstractSQL):
    def __init__(self, id, owner_id, applicant_id, answers=None):
        super().__init__("database.db")
        self.id = id 
        self.owner_id = owner_id #Job Post is Owner
        self.applicant_id = applicant_id #User is Applicant
        self.answers = json.loads(answers) or [] #Ignore for now

    def get_owner(self):
        from SQL.JobPost import JobPost
        raw = self.use_database(
            f"SELECT * FROM jobPost where owner_id", (self.owner_id,), easySelect=False
        )
        return [JobPost(*row) for row in raw][0] #should return 1 org; each post MUST have an owner
    
    def get_user(self):
        from SQL.User import User
        raw = self.use_database(
            f"SELECT * FROM users where ID = ?", (self.applicant_id,), easySelect=False
        )

        return [User(*row) for row in raw][0]