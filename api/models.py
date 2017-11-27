
class User:
    def __init__(self, id, full_name, email, password):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password = password


class Event:
    def __init__(self, id,  name, address, start_date, end_date, user, description, category):
        self.name = name
        self.id = id
        self.address = address
        self.start_date = start_date
        self.end_date = end_date
        self.user = user
        self.description = description
        self.category = category



