import random


class Review:
    ''' This class represents a review.
       Instantiating an object of this class without parametres creates a random, valid review.
    '''
    # order of attributes matters
    ATTRIBUTES = ['reviewText', 'rating', 'recommended']
    REVIEW_TEXTS    = ['This is really good.', 'This is really bad.', 'This is OK.', "I have seen better."]
    # pre_defined_item is a name in the items array
    # attributes is a dictionary
    def __init__(self, pre_defined_review = None, attributes = None):
        if pre_defined_review is not None:
            attributes = get_review(pre_defined_review)
        else:
            attributes = {}
        for attribute in Review.ATTRIBUTES:
            try:
                setattr(self, attribute, attributes[attribute])
            except KeyError:
                setattr(self, attribute, self._getValueFor(attribute))
        # This will get set when the review is posted        
        self.reviewer = ""        

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
        return self._getRandomNumber() % 6
    
    def _getRandomRecommended(self):
        return self._getRandomNumber() % 2
   
    def __str__(self):
        return self.reviewText
     
     
# pre-defined reviews
# add more here if you need to...
reviews = [
    {'name': 'emptyReviewText', 'reviewText' : ''},
    {'name': 'zeroStarReview', 'rating' : '0'},
    {'name': 'oneStarReview', 'rating' : '1'},
    {'name': 'twoStarReview', 'rating' : '2'},
    {'name': 'threeStarReview', 'rating' : '3'},
    {'name': 'fourStarReview', 'rating' : '4'},
    {'name': 'fiveStarReview', 'rating' : '5'},    
]

def get_review(name):
    for review in reviews:
        if review['name'] == name:
            return review
    raise KeyError("\n Review %s is not defined, enter a valid review.\n" %name)