from SQL.abstractSQL import abstractSQL


class Organization(abstractSQL):
    def __init__(self, id, owner_id, name, industry, tagline=None, website=None, github_link=None, size=None, logo_url=None):
        super().__init__("database.db")
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.industry = industry
        self.tagline = tagline
        self.website = website
        self.github_link = github_link
        self.size = size
        self.logo_url = logo_url

    
    def getPosts(self, id=None):
        from SQL.JobPost import JobPost
        if (id != None):
            raw = self.use_database(
                "SELECT * from jobPost WHERE owner_id = ? AND id = ?", (self.id,id), easySelect=False
            )
            return [JobPost(*row) for row in raw]

        raw = self.use_database(
            "SELECT * from jobPost WHERE owner_id = ?", (self.id,), easySelect=False
        )
        return [JobPost(*row) for row in raw]
    
    def updateName(self, input):
        self.use_database(
            f"UPDATE organizations SET name = ? WHERE ID = ?;", (input, int(self.id),), easySelect=False
        )
        return self.get_organizations(id=self.id)

    def updateDetails(self, item, newData):
        self.use_database(
            f"UPDATE organizations SET {item} = ? WHERE ID = ?;", (newData, int(self.id),), easySelect=False
        )
        return self.get_organizations(id=self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "industry": self.industry,
            "tagline": self.tagline,
            "website": self.website,
            "github_link": self.github_link,
            "size": self.size,
            "logo_url": self.logo_url
        }
    
    def get_owner(self):
        from SQL.User import User
        raw = self.use_database(
            f"SELECT * FROM users where ID = {self.owner_id}", (), easySelect=False
        )

        return [User(*row) for row in raw][0]