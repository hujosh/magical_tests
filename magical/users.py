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
                  'firstName', 'lastName', 'internalName', "bio", "website", "tagline"]
    NAMES     =  ['Josh', 'David', 'Kyle', 'Emmanuel', 'Rohan', 'Russel', 'Goddard',
                   'Olton', 'Spencer', 'Phillips', 'Amadio', 'Calydris', "Smith", "Fong",
                  "Judy", "Linda", "Jai", "Bin", "Lucy", "Matthew", "Leigh", "Nick",
                  "Birnie", "James", "Erin", "Bernard", "Jeniffer", "Deb", "Jessica"]
    PASSWORD  = 'oryx*967'

    MAX_USERNAME = 18
    
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
        self.fullName = ('%s %s'%(self.firstName, self.lastName)).strip()
        # These attributes allows a user to interact with the website via http requests.
        firstNames = self.firstName.split()
        if len(firstNames) > 0:
            self.firstName = self.firstName.split()[0]
        if len(firstNames) > 1:
            self.lastName = "".join(firstNames[1::])
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
                  'bio'             :self._getBio,
                  'website'         :self._getWebsite,
                  'tagline'         :self._getTagline,
                 }
        return switch[value_for]()
        
    def _getRandomNumber(self):
        return int(random.random()*99999999)
        
    def setFirstName(self, name, shouldTrim = True):
        self.firstName = name
        fullName = ('%s %s'%(self.firstName, self.lastName))
        if shouldTrim:
            fullName = fullName.strip()
        self.fullName = fullName
        
    def setLastName(self, name,shouldTrim = True):
        self.lastName = name
        fullName = ('%s %s'%(self.firstName, self.lastName))
        if shouldTrim:
            fullName = fullName.strip()
        self.fullName = fullName

    def _getWebsite(self):
        return "dev.magic.al"

    def _getBio(self):
        return "I was created to test magical"

    def _getTagline(self):
        return "What's a tagline?"


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
    {"name":"funnyCharInFirstName", "firstName" : "Pökémön"},
    {"name": "funnyCharInLastName", "lastName": "Pökémön"},
    {"name": "emptyName", "lastName": "", "firstName":""},
    {"name": "davidGoddard", "firstName" : "David", "lastName": "Goddard"}, #may need to recreate this user if the account gets deleted
    {"name": "threePartname", "lastName": "Butz", "firstName": "Dr Frank"},

]

def get_user(name):
    for user in users:
        if user['name'] == name:
            return user
    raise KeyError("\n User %s is not defined, enter a valid user.\n" %name)

    
