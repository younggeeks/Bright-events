from helpers import user_parser, event_parser
from models import User, Event


class DataMocks():

    users = [
        User(id=2, full_name="samwel Charles", email="younggeeks101@gmail.com", password="secret"),
        User(id=4, full_name="Michael Makopa", email="owirimichael@kiu.ac.tz", password="password"),
        User(id=43, full_name="Juma Yusuph", email="madongo@yahoo.com", password="new_password"),
        User(id=76, full_name="Deo Mwingereza", email="deo@chyna.com", password="mwingereza"),
        User(id=5634, full_name="Justus Micah", email="jmicah@jerusalem.com", password="ThouShaltNotPeep"),
        User(id=55, full_name="Renatus John", email="kinate@ymail.com", password="msukumahalisi")
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
        Event(id=9494, name="Angular Conference 2018", address="riverroad, Nairobi",
              start_date="1/3/2018", end_date="2/3/2018", user="Samwel Charles", description=
              "Come and Meet All These awesome developers and up your game", category="Meetup"),
        Event(id=894, name="Women Developers Pary", address="kirinyaga, Kenya",
              start_date="9/13/2019", end_date="9/15/2019", user="Samwel Charles", description=
              "Tech ladies , get your geek on , we'll be meeting and cofee will be free", category="Meetup"),
        Event(id=987, name="Acoustic Night", address="Magomeni, Dar es salaam",
              start_date="14/3/2019", end_date="2/3/2018", user="juma junior", description=
              "Come with your Guitar we are going to rock the night away with rock and roll on acoustic",
              category="Music"),
        Event(id=5221, name="Christ Ambassadors General Meeting", address="Chanika, Dar es salaam",
              start_date="2/3/2019", end_date="4/8/2019", user="Atanasi John", description=
              "Come one come all, let us meet and discuss matters that patterns to our youth", category="Religion"),
    ]

    @staticmethod
    def update_users(new_list):
        DataMocks.users = new_list
        print len(DataMocks.users)

    @staticmethod
    def update_events(new_events):
        DataMocks.events = new_events
        print len(DataMocks.events)

    # helper function that converts List of  Models to List of Dictionaries
    def get_data(self, data=None):
        if self == 'users':
            dict_users = []
            if data is not None:
                for user in data:
                    dict_users.append(user_parser(user))
                return dict_users
            else:
                for user in self.users:
                    dict_users.append(user_parser(user))

                return dict_users
        else:
            events_list = []
            for event in self.events:
                events_list.append(event_parser(event))
            return events_list
