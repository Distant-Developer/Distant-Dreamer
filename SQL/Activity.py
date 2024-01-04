from datetime import datetime


class Activity:
    def __init__(self, id, associated_id, activity_type, date):
        self.id = id
        self.associated_id = associated_id
        self.type = activity_type
        self.date = self.parseDate(date)

    def parseDate(self, input):
        return datetime.strptime(input, "%Y-%m-%d %H:%M:%S")