import random
import string


class Item:
    ''' This class represents an item.
       Instantiating an object of this class without parametres creates a random, valid item.
    '''
    # order of attributes matters
    ATTRIBUTES = ['itemName', 'price', 'friends', 'occasions',
                  'location', 'privacy', 'description', 'qty', 'validatedItemName', 'validatedItemPrice']
    NAMES      = ['car', 'computer', 'playstation', 'xbox', 'book']
    # pre_defined_item is a name in the items array
    # attributes is a dictionary
    def __init__(self, pre_defined_item = None, attributes = None):
        if pre_defined_item is not None:
            attributes = get_item(pre_defined_item)
        else:
            attributes = {}
        for attribute in Item.ATTRIBUTES:
            try:
                setattr(self, attribute, attributes[attribute])
            except KeyError:
                setattr(self, attribute, self._getValueFor(attribute))

    def _getRandomName(self):
        return random.choice(Item.NAMES) + str(self._getRandomNumber())
        
    def _getRandomPrice(self):
        return str(round(random.random() * 999999, 2))
      
    def _getValueFor(self, value_for):
        switch = {
                  'itemName'           : self._getRandomName,
                  'price'              : self._getRandomPrice,
                  'friends'            : str,
                  'occasions'          : str,
                  'location'           : str,
                  'privacy'            : self._getItemPrivacy,
                  'description'        : self._getItemDescription,
                  'qty'                : self._getRandomQty,
                  'by'                 : str,
                  'validatedItemName'  : self._getValidatedItemName,
                  'validatedItemPrice' : self._getValidatedItemPrice,
                 }
        return switch[value_for]()
        
    def _getRandomNumber(self):
        return int(random.random()*9999)
        
    def _getItemPrivacy(self):
        return 'myfriends'
        
    def _getItemDescription(self):
        return 'This item is called %s'%(self.itemName)
    
    def _getRandomQty(self):
        return self._getRandomNumber()
        
    def _getValidatedItemName(self):
        # Remove trailing and leading white space
        return self.itemName.strip()
        
    def _getValidatedItemPrice(self):
        # Whatever gets put in into the price field, only numbers, commas and a decimal can come out.
        punctuation = string.punctuation.replace(",", "")
        punctuation = punctuation.replace(".", "")
        punctuation = punctuation.replace("$", "")
        validation_string = "%s %s"%(string.ascii_letters, punctuation)
        self.price = self._roundDown(self.price)
        try:
            return str("${:,.2f}".format(float(self.price.strip(validation_string))))
        except:
            return '$0.00'

    def _roundDown(self, price):
      return price[:8]
 
    def __str__(self):
        return self.itemName
     
     
# pre-defined items
# add more here if you need to...
items = [
    {'name' : 'priceIsEmpty', 'price'  : ''},
    {'name' : 'priceHasLetters', 'price' : '2a'},
    {'name' : 'priceTooLarge', 'price'   : '9999999999999'},
    {'name' : 'priceHas3DecimalPlaces', 'price' : '44.994'},
    {'name' : 'itemNameIsEmpty', 'itemName' : '', "validatedItemName" : "No name entered"},
    {'name' : 'itemNameHasNumbersAndLetters', 'itemName' : 'name123name'},
    {'name' : 'itemNameHasOnlyNumbers', 'itemName' : '123'},
    {'name' : 'itemNameContainsOnlyZero', 'itemName' : '0'},
    {'name' : 'itemNameContainsOnlyNegative1', 'itemName' : '-1'},
    {'name' : 'itemNameContainsOnlyASpace', 'itemName' : ' ', "validatedItemName" : "No name entered"},
    {'name' : 'priceIsNegative', 'price' : '-4'},
    {'name' : 'priceIsZero', 'price' : '0'},
    {'name' : 'itemNameHasFunnyCharacters' , 'itemName' : 'Pökémön'}
]


def get_item(name):
    for item in items:
        if item['name'] == name:
            return item
    raise KeyError("\n Item %s is not defined, enter a valid item.\n" %name)