import json

class SpecialBadge:
    def __init__(self, name, style):
        self.name = name
        self.style = style

def fetch(id):
    return find_by_id(read_json(), id)

def read_json():
    with open("Utils/customBadges.json") as f: 
        return json.loads(f.read())
    
def find_by_id(data, target_id):
    try:
        badges = data[str(target_id)]
        badgesUserHas = []  # Use a simple list without specifying the type

        for badge in badges:
            badgesUserHas.append(SpecialBadge(name=badge, style=data["badges"][badge]["style"]))

        return badgesUserHas
    except:
        return None
