class Experience:
    def __init__(self, id, associated_user_id, company_name, company_logo_url, position_title, position_description, dates):
        self.id = id
        self.associated_user_id = associated_user_id
        self.company_name = company_name
        self.company_logo_url = company_logo_url
        self.position_title = position_title
        self.position_description = position_description
        self.dates = dates