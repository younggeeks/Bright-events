
class User:
    """
    Model class for User
    """
    def __init__(self, id, full_name, email, password):
        """
        constructor which will be called every time User object is instantiated
        :param id:
        :param full_name:
        :param email:
        :param password:
        """
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password = password


class Event:
    """
    Model class for Event
    """
    def __init__(self, id,  name, address, start_date, end_date, user, description, category):
        """
        constructor which will be called every time User object is instantiated
        :param id:
        :param name:
        :param address:
        :param start_date:
        :param end_date:
        :param user:
        :param description:
        :param category:
        """
        self.name = name
        self.id = id
        self.address = address
        self.start_date = start_date
        self.end_date = end_date
        self.user = user
        self.description = description
        self.category = category



