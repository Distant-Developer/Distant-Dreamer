import json
import os

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
    badges = data.get(str(target_id))

    if badges is not None:
        # Use a list comprehension for a more concise and efficient way to create the list
        badgesUserHas = [SpecialBadge(name=badge, style=data["badges"][badge]["style"]) for badge in badges]

        return badgesUserHas

    return None


if __name__ == "__main__":
    file_path = "Utils/customBadges.json"
    if not os.path.exists(file_path):
        # Create an empty dictionary (you can modify this as needed)
        data_to_write = {}

        # Write the data to the file
        with open(file_path, 'w') as file:
            json.dump(data_to_write, file)

        print(f"The file '{file_path}' has been created.")
    else:
        print(f"The file '{file_path}' already exists.")