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