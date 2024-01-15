import json
import re
from SQL.Education import Education
from SQL.Experience import Experience
from SQL.abstractSQL import abstractSQL

class User(abstractSQL):
    def __init__(self, id, token, username, email, is_verified, is_staff, linkedin_url=None, github_url=None, discord=None, description=None, logo_url=None, type=None):
        super().__init__()
        self.id = id
        self.token = token
        self.username = username
        self.email = email
        self.is_staff = self.int_to_bool(is_staff)
        self.is_verified = self.int_to_bool(is_verified)
        self.linkedin_url = linkedin_url
        self.github_url = github_url
        self.discord = discord
        self.description = self.remove_scripts(description)
        self.logo_url = logo_url
        self.type = type

        self.education = self.get_educations()
        self.experience = self.get_experiences()

    def get_experiences(self):
        list = self.use_database(
            "SELECT * from experiences where owner_id = ?", (self.id,), easySelect=False
        )

        return [Experience(*row) for row in list]
    
    def get_educations(self):
        list = self.use_database(
            "SELECT * from educations where owner_id = ?", (self.id,), easySelect=False
        )

        return [Education(*row) for row in list]
    
    def get_posts(self):
        from SQL.Post import Post
        raw = self.use_database(
            "SELECT * from posts where owner_id = ?", (self.id,), easySelect=False
        )
        return [Post(*row) for row in raw]
    
    def get_organizations(self):
        raw = self.use_database(
            "SELECT * from organizations where owner_id = ?", (self.id,), easySelect=False
        )
        from SQL.Organization import Organization

        return [Organization(*row) for row in raw]
    
    def has_organization(self):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()


        self.cursor.execute("SELECT COUNT(*) FROM organizations WHERE owner_id = ?", (self.id,))
        count = self.cursor.fetchone()[0]

        self.close()
        state: bool = count >= 1

        return state

    

    def to_dict(self):
            return {
                "id": self.id,
                "token": self.token,
                "username": self.username,
                "email": self.email,
                "is_verified": self.is_verified,
                "is_staff": self.is_staff,
                "linkedin_url": self.linkedin_url,
                "github_url": self.github_url,
                "description": self.description,
            }
    
    
    def int_to_bool(self, input):
        if input == 0: 
            return False 
        elif input == 1:
            return True
    
    def Linkedin_isNotEmpty(self):
        return self.linkedin_url != None
    
    def Github_isNotEmpty(self):
        return self.github_url != None
    
    def Discord_isNotEmpty(self):
        return self.discord != None
    
    def remove_scripts(self, input_string):
        if input_string == "" or input_string == None:
            return
        # Define the pattern for matching <script> ... </script>
        script_pattern = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL)

        # Use sub() method to replace matched patterns with an empty string
        result_string = re.sub(script_pattern, '', input_string)

        return result_string
    
    def is_not_verified(self):
        not_verified = not self.is_verified
        return not_verified 
    
    def has_email(self):
        return self.email != None