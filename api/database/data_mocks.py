from database.models import User, Event
from helpers import user_parser, event_parser


class DataMocks:

    def __init__(self):
        pass

    users = [
        User(id=2, full_name="samwel", email="younggeeks101@gmail.com", password="secret"),
        User(id=4, full_name="junior", email="owirimichael@kiu.ac.tz", password="password"),
        User(id=43, full_name="michael", email="madongo@yahoo.com", password="new_password"),
        User(id=76, full_name="juma", email="deo@chyna.com", password="mwingereza"),
        User(id=5634, full_name="atanasi", email="jmicah@jerusalem.com", password="ThouShaltNotPeep"),
        User(id=55, full_name="john", email="kinate@ymail.com", password="msukumahalisi")
    ]

    rsvps = [
        {
            "event_id": 9494,
            "users": [
                User(id=2, full_name="samwel Charles", email="younggeeks101@gmail.com", password="secret")
            ]
        },
        {
            "event_id": 987,
            "users": [
                User(id=2, full_name="samwel Charles", email="younggeeks101@gmail.com", password="secret")
            ]
        }
    ]

    events = [
        Event(id=9494, price = 89389, name="Angular Conference 2018", address="Riverroad, Nairobi",
              start_date="1/3/2018", end_date="2/3/2018", user="samwel", description=
              "Come and Meet All These awesome developers and up your game", category="Meetup"),
        Event(id=894, name="Women Developers Pary", price = 100, address="kirinyaga, Kenya",
              start_date="9/13/2019", end_date="9/15/2019", user="atanasi", description=
              "Tech ladies , get your geek on , we'll be meeting and cofee will be free", category="Meetup"),
        Event(id=987, name="Acoustic Night", price = 2000, address="Magomeni, Dar es salaam",
              start_date="14/3/2019", end_date="2/3/2018", user="juma", description=
              "Come with your Guitar we are going to rock the night away with rock and roll on acoustic",
              category="Music"),
        Event(id=5221, name="Geeks General Meeting", price = 10009, address="Chanika, Dar es salaam",
              start_date="2/3/2019", end_date="4/8/2019", user="samwel", description=
              "Come one come all, let us meet and discuss matters that patterns to our youth", category="Religion"),
    ]

    @staticmethod
    def update_users(new_list):
        """
        Method that will update our users List , When called It will replace current list with new list
        which was passed as an argument , It'll be called when update or delete is called
        :param new_list:
        :return:
        """
        DataMocks.users = new_list

    @staticmethod
    def update_events(new_events):
        """
        Method that will update our events List , When called It will replace current list with new list
        which was passed as an argument , It'll be called when update or delete is called
        :param new_events:
        :return:
        """
        DataMocks.events = new_events

    @staticmethod
    def get_data(data_type, data=None):
        """
        Helper function which will be responsible for converting(parsing) list of either User or Data models
        to list of dictionaries, caller will pass in string argument(data_type) with value of either
        "users" or "events" and optional data argument , if data argument is not specified it will be
        defaulted to None , meaning function will convert users or events list from our dummy data , if data
        argument is passed, data that will be passed will be parsed accordingly .
        :param data_type:
        :param data:
        :return parsed_dictionary:
        """
        if data_type == 'users':
            dict_users = []
            if data is not None:
                for user in data:
                    dict_users.append(user_parser(user))
                return dict_users
            else:
                for user in DataMocks.users:
                    dict_users.append(user_parser(user))

                return dict_users
        else:
            events_list = []
            if data is not None:
                for event in data:
                    events_list.append(event_parser(event))
                return events_list
            else:
                for event in DataMocks.events:
                    events_list.append(event_parser(event))
                return events_list
