import re


class User:
    def __init__(self, id, token, username, email, is_staff=0, is_verified=0, linkedin_url=None, github_url=None, description=None):
        self.id = id
        self.token = token
        self.username = username
        self.email = email
        self.is_verified = self.int_to_bool(is_verified)
        self.is_staff = self.int_to_bool(is_staff)
        self.linkedin_url = linkedin_url
        self.github_url = github_url
        self.description = self.remove_scripts(description)

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
        else: 
            return True
    
    def Linkedin_isNotEmpty(self):
        return self.linkedin_url != None
    
    def Github_isNotEmpty(self):
        return self.github_url != None
    
    def remove_scripts(self, input_string):
        if input_string == "" or input_string == None:
            return
        # Define the pattern for matching <script> ... </script>
        script_pattern = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL)

        # Use sub() method to replace matched patterns with an empty string
        result_string = re.sub(script_pattern, '', input_string)

        return result_string