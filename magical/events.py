import random
import string
from datetime import datetime


class Event:
    ''' This class represents an item.
       Instantiating an object of this class without parametres creates a random, valid item.
    '''
    ATTRIBUTES = ['eventName', 'date', 'remindMe', 'remindMeDays',
                  'privacy', 'host', 'invitees']
    NAMES = ['Christmas', "Easter", "Lent",  "Yule", "Allhallowtide"]

    # pre_defined_item is a name in the items array
    # attributes is a dictionary
    def __init__(self, pre_defined_event=None, attributes=None):
        if pre_defined_event is not None:
            attributes = get_event(pre_defined_event)
        else:
            attributes = {}
        for attribute in Event.ATTRIBUTES:
            try:
                setattr(self, attribute, attributes[attribute])
            except KeyError:
                setattr(self, attribute, self._getValueFor(attribute))

    def _getRandomName(self):
        return random.choice(Event.NAMES)

    def _getRandomDate(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        return datetime(current_year,current_month,current_day)

    def _getRandmoBool(self):
        return random.choice([True, False])

    def _getRandomPrivacy(self):
        return random.choice(["Only me", "Friends", "Anyone")


    def _getRandomHost(self):
        return None

    def _getRandomInvitees(self):
        return None

    def _getValueFor(self, value_for):
        switch = {
            'eventName': self._getRandomName,
            'date': self._getRandomDate,
            'remindMe': self.self._getRandomBool,
            'remindMeDays': self._getRandomNumber,
            'privacy': self._getRandomPrivacy,
            'host': self._getRandomHost,
            'invitees': self._getRandomInvitees,
        }
        return switch[value_for]()

    def _getRandomNumber(self):
        return int(random.random() * 9999)

    def __str__(self):
        return self.eventName


# pre-defined events
# add more here if you need to...
events = [
    {"name": "emptyName", "eventName": ""},
]


def get_event(name):
    for event in events:
        if event['name'] == name:
            return event
    raise KeyError("\n Event %s is not defined, enter a valid event.\n" % name)