class Education:
    def __init__(self, id, associated_user_id, tuition_name, tuition_logo_url, position_description, dates):
        self.id = id
        self.owner_id = associated_user_id
        self.tuition_name = tuition_name
        self.tuition_logo_url = tuition_logo_url
        self.tuition_description = position_description
        self.dates = dates