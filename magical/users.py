import random
import time

from webapi.awebapi import AHTTP
# HTTP is synchronous, AHTTP is asynchronous. The former is used for functional testing, the latter for load testing.
from webapi.webapi import HTTP


class User:
    '''Represents a user of the app.
       Creating an object of this class with no parametres creates a random user.
    '''
    # order of attributes matters
    ATTRIBUTES = ['username', 'email', 'password', 'retypedPassword',
                  'firstName', 'lastName', 'internalName']
    NAMES     =  ['Josh', 'David', 'Kyle', 'Emmanuel', 'Rohan', 'Russel', 'Goddard',
                   'Olton', 'Spencer', 'Phillips', 'Amadio', 'Calydris']
    PASSWORD  = 'oryx*967'
    
    # pre_defined_user is a name in the users array
    # attributes is a dictionary
    def __init__(self, pre_defined_user = None, attributes = None):
        if pre_defined_user is not None:
            attributes = get_user(pre_defined_user)
        else:
            attributes = {}
        for attribute in User.ATTRIBUTES:
            try:
                setattr(self, attribute, attributes[attribute])
            except KeyError:
                setattr(self, attribute, self._getValueFor(attribute))
        self.fullName = '%s %s'%(self.firstName, self.lastName)
        # These attributes allows a user to interact with the website via http requests.
        self.http = HTTP(self)
        self.ahttp = AHTTP(self)
        
    def _getRandomUsername(self):
        current_unix_epoch = int(time.time())
        return '%s%s'%(current_unix_epoch, self._getRandomNumber())
    
    def _getRandomEmail(self):
        return 'joshua+%s@magic.al'%(self._getRandomNumber())
        
    def _getPassword(self):
        return User.PASSWORD
  
    def _getRandomFirstName(self):
        return random.choice(User.NAMES)
        
    def _getRandomLastName(self):
        return random.choice(User.NAMES)
    
    def _getInternalName(self):
        '''This is how your name appears to yourself in the app'''
        return 'Me'

    def _getValueFor(self, value_for):
        switch = {'email'           : self._getRandomEmail,
                  'username'        : self._getRandomUsername,
                  'password'        : self._getPassword,
                  'retypedPassword' : self._getPassword,
                  'firstName'       : self._getRandomFirstName,
                  'lastName'        : self._getRandomLastName,
                  'internalName'    : self._getInternalName,
                 }
        return switch[value_for]()
        
    def _getRandomNumber(self):
        return int(random.random()*99999999)
        
    def setFirstName(self, name):
        self.firstName = name
        self.fullName = '%s %s'%(self.firstName, self.lastName)
        
    def setLastName(self, name):
        self.lastName = name
        self.fullName = '%s %s'%(self.firstName, self.lastName)

        
# pre-defined users
# add more here if you need to...
users = [
	{"name": "extantUser", "email": "joshua@magic.al", "password": "oryx*967", 'username' : 'joshgoddard',
        "firstName" : "j" , "lastName" : "goddard"},
    {"name": "emptyEmail", "email": ""},
    {"name": "emptyPassword", "email": "joshua@magic.al", "password": ""},
    {"name": "nonExistentUser", "email": "joshuaz@magic.al", "password": "oryx*967"},
    {"name": "longEmail", "email": "joshuaz"*15+"@magic.al", "password": "oryx*967"},
    {"name": "emptyEmailAndPassword", "email": "", "password": ""},
    {"name": "usernameTooLong", "username": "abc123abc123abc123z"},
    {"name": "emptyPasswords", "password": "", "retypedPassword" : ""},
    {"name": "passwordsDontMatch", "password": "password1", "retypedPassword": "password2"},
    {"name": "emptyPassword", "password": ""},
    {"name": "emptyUsername", "username": ""},
    {"name": "emptyFirstName", "firstName": ""},
    {"name": "emptyLastName", "lastName": ""},
    {"name": "invalidEmail", "email": "aaaaazasaasadasf"},
    {"name": "emptyRetypedPassword", "retypedPassword": ""},
    {"name": "emptyLastNameEmptyEmail", "lastName": "", "email":""},
    {"name": "random"},
]

def get_user(name):
    for user in users:
        if user['name'] == name:
            return user
    raise KeyError("\n User %s is not defined, enter a valid user.\n" %name)
    
    
def test(user):
        item = Item()
        user.http.addItem(item)    
    
if __name__ == '__main__':
    
    
    user1 = User('extantUser')
    user2 = User('extantUser')

    p = Pool(1)
    start = time.time()
    for request in p.imap_unordered(test, [user1, user2]):
        print("{} (Time elapsed: {}s)".format(request, int(time.time() - start))) 