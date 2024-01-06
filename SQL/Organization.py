class Organization:
    def __init__(self, id, owner_id, name, industry, tagline=None, website=None, github_link=None, size=None, logo_url=None):
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.industry = industry
        self.tagline = tagline
        self.website = website
        self.github_link = github_link
        self.size = size
        self.logo_url = logo_url

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
            "logo_url": self.logo_url,
        }