class User:
    def __init__(self, id, token, username, email, is_staff=False, linkedin_url=None, github_url=None, description=None):
        self.id = id
        self.token = token
        self.username = username
        self.email = email
        self.is_staff = self.int_to_bool(is_staff)
        self.linkedin_url = linkedin_url
        self.github_url = github_url
        self.description = description

    def int_to_bool(self, input):
        if input == 0: 
            return False 
        else: 
            return True