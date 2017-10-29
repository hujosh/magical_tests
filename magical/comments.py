import random


class Comment:
    ''' This class represents an review.
       Instantiating an object of this class without parametres creates a random, valid review.
    '''
    # order of attributes matters
    ATTRIBUTES = ['commentText', 'rating', 'recommended']
    REVIEW_TEXTS    = ['This is really good.', 'This is really bad.', 'This is OK.', "I've seen better."]
    # pre_defined_item is a name in the items array
    # attributes is a dictionary
    def __init__(self, pre_defined_comment = None, attributes = None):
        if pre_defined_comment is not None:
            attributes = get_review(pre_defined_review)
        else:
            attributes = {}
        for attribute in Review.ATTRIBUTES:
            try:
                setattr(self, attribute, attributes[attribute])
            except KeyError:
                setattr(self, attribute, self._getValueFor(attribute))

    def _getRandomReviewText(self):
        return random.choice(Review.REVIEW_TEXTS)
         
    def _getValueFor(self, value_for):
        switch = {
                  'reviewText'  : self._getRandomReviewText,
                  'rating'      : self._getRandomRating,
                  'recommended' : self._getRandomRecommended,
                 }
        return switch[value_for]()
        
    def _getRandomNumber(self):
        return int(random.random()*9999)
        
    def _getRandomRating(self):
        return self._getRandomNumber() % 5
    
    def _getRandomRecommended(self):
        return self._getRandomNumber() % 2
   
    def __str__(self):
        return self.reviewText
     
     
# pre-defined reviews
# add more here if you need to...
reviews = [
    {'name': 'emptyReviewText', 'reviewText' : ''},
    
]

def get_review(name):
    for review in reviews:
        if review['name'] == name:
            return review
    raise KeyError("\n Review %s is not defined, enter a valid review.\n" %name)