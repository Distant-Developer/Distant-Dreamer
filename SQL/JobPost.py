from SQL.abstractSQL import abstractSQL


class JobPost(abstractSQL):
    def __init__(self, id, owner_id, position_title, position_content, app_url, archived, hidden):
        super().__init__("database.db")
        self.id = id
        self.owner_id = owner_id
        self.position_title = position_title
        self.position_content = position_content
        self.app_url = app_url
        self.archived = self.int_to_bool(archived)
        self.hidden = self.int_to_bool(hidden)

    def __repr__(self):
        return f"JobPost(id={self.id}, owner_id={self.owner_id}, position_title='{self.position_title}', position_content='{self.position_content}', app_url='{self.app_url}')"
    
    
    def archive(self):
        self.use_database(
            f"UPDATE jobPost SET archived = 1 WHERE id = ?;", 
            (   
                self.id,
            ),
        )

    def hide(self):
        self.use_database(
            f"UPDATE jobPost SET hidden = 1 WHERE id = ?;", 
            (   
                self.id,
            ),
        )
        
    def get_owner(self):
        from SQL.Organization import Organization
        raw = self.use_database(
            f"SELECT * FROM organizations where ID = {self.owner_id}", (), easySelect=False
        )

        return [Organization(*row) for row in raw][0] #should return 1 org; each post MUST have an owner