from database.models import User, Event
from helpers import user_parser, event_parser


class DataMocks:
    def __init__(self):
        pass

    users = [
        User(id=2, full_name="sam", email="younggeeks101@gmail.com", password="secret"),
        User(id=4, full_name="junior", email="owirimichael@kiu.ac.tz", password="password"),
        User(id=5, full_name="michael", email="madongo@yahoo.com", password="new_password"),
        User(id=6, full_name="juma", email="deo@chyna.com", password="mwingereza"),
        User(id=7, full_name="atanasi", email="jmicah@jerusalem.com", password="ThouShaltNotPeep"),
        User(id=8, full_name="john", email="kinate@ymail.com", password="msukumahalisi")
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
        Event(id=9494, price=89389, name="WOMEN WHO CODE", address="Riverroad, Nairobi",
              start_date="2017-12-16", end_date="2017-12-16", user="sam", description=
              "Women Who Code presents a Hackathon designed to showcase women as they take on tech. Join our "
              "community of changemakers for Nairobi Hackathon October 13-15, 2017 to make something great. A "
              "Hackathon like no other the WWCode ",
              category="Hackathon"),
        Event(id=894, name="Mobile Museum of Art", price=100, address="kirinyaga, Kenya",
              start_date="2017-12-16", end_date="2017-12-16", user="sam", description=
              "Did you know there are 17 museums in Mobile? Let's go visit all of them! We'll start with the Mobile "
              "Museum of Art for their free admission special. MMOFA is celebrating the opening of new art "
              "exhibits. They will have a free concert outdoors", category="Meetup"),
        Event(id=987, name="Fitness boot camp", price=2000, address="Magomeni, Dar es salaam",
              start_date="2017-12-16", end_date="2017-12-16", user="sam", description=
              "A fitness boot camp is a type of group physical training program conducted by gyms, personal trainers,"
              "and former military personnel. These programs are designed to build strength and fitness through a "
              "variety "
              " of intense group intervals over a 1-hour period of time",
              category="Bootcamps"),
        Event(id=5221, name="2017 Tech Bootcamp", price=10009, address="Chanika, Dar es salaam",
              start_date="2017-12-16", end_date="2017-12-16", user="sam", description=
              "We will be holding a one-week intensive hands-on Kids Tech Bootcamp during the April holidays. "
              "Training will be on: Electronics and Robotics; Web Programming and Design; Minecraft 3D game modding; "
              , category="Code Camps"),
        Event(id=5879, name="Fit Kenyan Bootcamp", price=10009, address="Mombasa, Kenya",
              start_date="2017-12-16", end_date="2017-12-16", user="sam", description=
              "Fit Kenyan Bootcamp has transformed, inspired and made people sweat since 2013! FKB was founded with "
              "the main aim to create an affordable work out regime with the concept to make use of our beautiful "
              , category="Code Camps"),
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
            return fetch_users(data)
        elif data_type == "events":
            print("data from get_data", data)
            return fetch_events(data)


def fetch_users(data):
    dict_users = []
    if data:
        [dict_users.append(user_parser(user)) for user in data]
        return dict_users
    else:
        [dict_users.append(user_parser(user)) for user in DataMocks.users]
        return dict_users


def fetch_events(data):
    print("data is ", data)
    events_list = []
    if data:
        [events_list.append(event_parser(event)) for event in data]
        return events_list
    else:
        [events_list.append(event_parser(event)) for event in DataMocks.events]
        return events_list
