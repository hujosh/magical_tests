import copy
import time

from selenium.webdriver.support import expected_conditions as EC

from mobile_app.base import ElementNotFound
from mobile_app.base import FriendNotFound
from mobile_app.base import ItemNotFound
from mobile_app.base import Section
from mobile_app.locators import *


class AlertSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = AlertSectionLocators
        super().__init__(driver, **kwargs)
        self.timeout = 1
        self.message = self.getMessage()
        self.title   = self.getTitle()
        
    def isSectionLoaded(self):
        self.findElement(* self.locator.ALERT_BOX)
        
    def getMessage(self):
        try:
            return self.findElement(*self.locator.MESSAGE).text
        except:
            return None
        
    def getTitle(self):
        try:
            return self.findElement(*self.locator.TITLE).text
        except:
            return None
        
    def pressCancel(self):
        self.findElement(*self.locator.CANCEL_BUTTON).click()
        self._PutAppInBackground()

    def pressOK(self):
        self.findElement(*self.locator.OK_BUTTON).click()
        self._PutAppInBackground()

    def pressSubmit(self):
        self.findElement(*self.locator.SUBMIT_BUTTON).click()
        self._PutAppInBackground()
    
    def pressConfirm(self):
        self.findElement(*self.locator.CONFIRM_BUTTON).click()
        self._PutAppInBackground()

    def enterInput(self, input):
        self.enterText(self.findElement(*self.locator.INPUT_FIELD), input)

    def pressYes(self):
        self.findElement(*self.locator.YES_BUTTON).click()
        self._PutAppInBackground()
    
    def pressNo(self):
        self.findElement(*self.locator.NO_BUTTON).click()
        self._PutAppInBackground()
        
        
class LoginSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = LoginSectionLocators
        self.activity = self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        
    def enterEmail(self, user):
        self.enterText(self.findElement(* self.locator.EMAIL_FIELD), user.email)
        
    def enterUsername(self, user):
        self.enterText(self.findElement(* self.locator.USERNAME_FIELD), user.username)
            
    def enterPassword(self, user):
        self.enterText(self.findElement(* self.locator.PASSWORD_FIELD), user.password)
        
    def pressForgotPassword(self):
        self.findElement(* self.locator.FORGOT_PASSWORD_BUTTON).click()
        return AlertSection(self.driver)

    def pressJoinUs(self):
        self.findElement(* self.locator.JOIN_US_BUTTON).click()
        return SignupSection(self.driver)
        
    def pressLogin(self):
        self.findElement(* self.locator.LOGIN_BUTTON).click()
        
    def loginSuccessfully(self, user, withEmail = True):
        if withEmail == True:
            self.enterEmail(user)
        else:
            self.enterUsername(user)
        self.enterPassword(user)
        self.pressLogin()
        # This is so we can keep tack of which user is logged in...
        self._setLoggedinUser(user)
        return MainSection(self.driver)
    
    def loginUnsuccessfully(self, user, withEmail = True):
        if withEmail == True:
            self.enterEmail(user)
        else:
            self.enterUsername(user)
        self.enterPassword(user)
        self.pressLogin()
        return AlertSection(self.driver)
         
         
class SignupSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = SignupSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
          
    def pressSignup(self):
        self.findElement(* self.locator.SIGNUP_BUTTON).click()
        
    def pressNext(self):
        self.findElement(* self.locator.NEXT_BUTTON).click()
         
    def enterUsername(self, user):
        self.enterText(self.findElement(* self.locator.USERNAME_FIELD), user.username)
    
    def pressUsername(self):
        self.findElement(* self.locator.USERNAME_FIELD).click()
        self.remove_keyboard()
    
    def enterEmail(self, user):
        self.enterText(self.findElement(* self.locator.EMAIL_FIELD), user.email)

    def enterPassword(self, user):
        self.enterText(self.findElement(* self.locator.PASSWORD_FIELD), user.password)
    
    def enterRetypedPassword(self, user):
        self.enterText(self.findElement(* self.locator.RETYPED_PASSWORD_FIELD), user.retypedPassword)
        
    def enterFirstName(self, user):
        self.enterText(self.findElement(* self.locator.FIRST_NAME_FIELD), user.firstName)
        
    def enterLastName(self, user):
        self.enterText(self.findElement(* self.locator.LAST_NAME_FIELD), user.lastName)    

    def signupSuccessfullyFirstPage(self, user):
        self.enterUsername(user)
        self.enterEmail(user)
        self.enterPassword(user)
        self.enterRetypedPassword(user)
        self.pressNext()
        return AlertSection(self.driver)
        
    def signupSuccessfullySecondPage(self, user):
        self.enterFirstName(user)
        self.enterLastName(user)
        self.pressSignup()
        return AlertSection(self.driver, timeout = 15)
        
    def signupUnsuccessfullyFirstPage(self, user):
        self.enterUsername(user)
        self.enterEmail(user)
        self.enterPassword(user)
        self.enterRetypedPassword(user)
        self.pressNext()
        return AlertSection(self.driver)
        
    def signupUnsuccessfullySecondPage(self, user):
        self.enterFirstName(user)
        self.enterLastName(user)
        self.pressSignup()
        return AlertSection(self.driver)
       
       
class MainSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = MainSectionLocators
        self.activity = MainSectionLocators.ACTIVITY
        super().__init__(driver, **kwargs)
       
    def pressPlus(self):
        self.findElement(* self.locator.PLUS_BUTTON).click()
        time.sleep(1)
        
    @property    
    def bigItemList(self):
        '''
        The main section of the app has the big item list that shows everything your friends want.
        '''
        return ItemListSection(self.driver)
        
    def pressAddItem(self):
        self.findElement(* self.locator.ADD_ITEM_BUTTON).click()
        return AddItemSection(self.driver, timeout = self.timeout)

    def pressAddFriend(self):
        self.findElement(* self.locator.ADD_FRIEND_BUTTON).click()
        return AddFriendSection(self.driver)

    def pressSettingsButton(self):
        self.findElement(* self.locator.SETTINGS_BUTTON).click()
        return SettingsSection(self.driver)     
              
              
class ItemListSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = ItemListSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        #self.context = self._getContext()
        # Let's scroll quickly through the item list rather than waiting 5 seconds for each item...
        self.timeout = 0.5
        
    def isSectionLoaded(self):
        super().isSectionLoaded()
        self.findElement(* self.locator.ITEM_LIST)
        
    def findItem(self, find_item, nscrolls = 5):
        '''Scroll through the item list nscroll times until find_item is found.'''
        if not(self.itemListEmpty):
            i = 0
            while i < nscrolls:
                items = self.findElements(*self.locator.ITEM)
                for item in items:
                    try:
                        name = self.findElementFromElement(self.locator.ITEM_NAME_TEXT, item).text
                        by   = self.findElementFromElement(self.locator.BY_TEXT, item).text
                        if find_item['name'] == name and (('By '+ find_item['by']) == by):
                            find_item['element'] = item
                            return find_item
                    except ElementNotFound:
                        pass
                i += 1            
                self.flick('down')
        raise ItemNotFound('Could not find the item with name "%s" by "%s" in item list'%(find_item['name'], find_item['by']))
        
    def pressItem(self, item):
        item = self.findItem(item)
        item['element'].click()
        return ViewItemSection(self.driver)
        
    def _getContext(self):
        return self.findElement(* self.locator.ITEM_LIST_CONTEXT).text
        
    @property    
    def itemListEmpty(self):
        try:
            self.findElement(*self.locator.NO_ITEMS_FOUND_TEXT).text
            return True
        except:
            return False
        
        
class FriendItemListSection(ItemListSection):   
    def __init__(self, driver, **kwargs):
        self.locator = FriendItemListSectionLocators
        self.activity =  self.locator.ACTIVITY
        Section.__init__(self, driver, **kwargs)
        #self.context = self._getContext()
        # Let's scroll quickly through the item list rather than waiting 5 seconds for each item...
        self.timeout = 0.5
    
    
class HorizontalFriendsListSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = HorizontalFriendsListSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
         
    def isSectionLoaded(self):
        super().isSectionLoaded()
        self.findElement(* self.locator.FRIENDS_LIST)
        
    def friendInList(self, friend, nscrolls = 3):
        if nscrolls == 0:
            return False
        friend_images = self.findElements(*self.locator.FRIEND)
        names = [name.text for name in self.findElements(*self.locator.FRIEND_NAME)]
        for friend_image,name in zip(friend_images, names):
            if name == friend.firstName:
                self.friend = friend_image
                return True
       #self.flick("right")
        self.scroll(friend_images)
        nscrolls -= 1
        return self.friendInList(friend,nscrolls)
         
    def pressFriend(self, friend):
        if self.friendInList(friend):
            self.friend.click()
            return FriendSection(self.driver)
        else:
            raise FriendNotFound("Could not find '%s' in the horizontal friends list."%friend.firstName)
     
    def pressMe(self, friend):
        friends = self.findElements(*self.locator.FRIEND)
        # I (me) is the first friend
        friends[0].click()
        return LoggedinUserSection(self.driver)    

    def pressRightArrow(self):
        self.findElement(*self.locator.RIGHT_ARROW_BUTTON).click()
        return VerticalFriendsListSection(self.driver)
        
        
class VerticalFriendsListSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = VerticalFriendsListSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        
    def friendInList(self, friend, nscrolls = 3):
        if nscrolls == 0:
            return False
        friends = self.findElements(*self.locator.FRIEND, 
            expectedCondition = EC.presence_of_all_elements_located)
        for friend_element in friends:
            name = self.findElementFromElement(self.locator.FRIEND_NAME_TEXT, friend_element,
                EC.presence_of_element_located).text
            if name == friend.fullName:
                self.friend = friend_element
                return True                
        self.flick('down')
        nscrolls -= 1
        return self.friendInList(friend, nscrolls)

    def pressFriend(self,friend):
        if self.friendInList(friend):
            self.friend.click()
        else:
            raise FriendNotFound("Coud not find '%s' in the vertical friends list"%friend.fullName)
        return FriendSection(self.driver)
    
    def pressMe(self, friend):
        me = copy.copy(friend)
        me.firstName = friend.internalName
        me.lastName = ""
        me.fullName = friend.internalName
        self.pressFriend(me)
        return LoggedinUserSection(self.driver)    
            
            
class AddItemSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = AddItemSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
    
    def pressAddItem(self):
        self.findElement(* self.locator.ADD_ITEM_BUTTON).click()
        
    def enterItemName(self, item):
        self.enterText(self.findElement(* self.locator.ITEM_NAME_FIELD), item.itemName)
        
    def enterItemPrice(self, item):
        self.enterText(self.findElement(* self.locator.PRICE_FIELD), item.price)
        
    def _addItem(self, item):
        self.enterItemName(item)
        self.enterItemPrice(item)
        self.flick("down")
        
    def addItemUnsuccessfully(self, item):
        self._addItem(item)
        self.pressAddItem()
        return AlertSection(self.driver)

    def addItemSuccessfully(self, item):
        self._addItem(item)
        self.pressAddItem()
        return MainSection(self.driver)
        

class ViewItemSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = ViewItemSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        
    @property
    def price(self):
        return self.findElement(* self.locator.PRICE_TEXT).text
        
    @property
    def reviewList(self):
        return ReviewListSection(self.driver)
        
    def pressAddReviewButton(self):
        self.findElement(* self.locator.ADD_REVIEW_BUTTON).click()
        return ReviewSection(self.driver)

    def pressEditItem(self):
        self.findElement(*self.locator.EDIT_BUTTON).click()


class ReviewListSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = ReviewListSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
          
    def reviewInList(self, review, nscrolls = 3):
        if nscrolls == 0:
            return False
        reviews = self.findElements(*self.locator.REVIEW)
        for review_element in reviews:
            reviewer = self.findElementFromElement(self.locator.REVIEWER_TEXT, review_element).text
            review_message = self.findElementFromElement(self.locator.REVIEW_TEXT, review_element).text
            if review_message == review.reviewText and self.loggedinUser.fullName in reviewer:
                return True
        self.flick("down")
        nscrolls -= 1
        return self.reviewInList(review,nscrolls)
         
         
class SettingsSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = SettingSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)    
        
    def pressLogoutButton(self): 
        self.findElement(* self.locator.LOG_OUT_BUTTON).click()
        
        
class ReviewSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = ReviewSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)

    def enterReviewText(self, review):
        self.enterText(self.findElement(*self.locator.REVIEW_TEXT_FIELD), review.reviewText)

    def pressPostReview(self):
        self.findElement(* self.locator.POST_REVIEW_BUTTON).click()
        
    def enterRating(self, review):
        rating = int(review.rating)
        if  rating == 1:
            self.findElement(* self.locator.ONE_STAR_BUTTON).click()
        elif rating == 2:
            self.findElement(* self.locator.TWO_STAR_BUTTON).click()
        elif rating == 3:
            self.findElement(* self.locator.THREE_STAR_BUTTON).click()
        elif rating == 4:
            self.findElement(* self.locator.FOUR_STAR_BUTTON).click()
        elif rating == 5:
            self.findElement(* self.locator.FIVE_STAR_BUTTON).click()
        # if rating == 0, we do nothing...    
            
    def _addReview(self, review):
        self.enterReviewText(review)
        self.enterRating(review)
        self.pressPostReview()
        time.sleep(2)
        
    def addReviewSuccessfully(self, review):
        self._addReview(review)
        return ViewItemSection(self.driver)
             
    def addReviewUnsuccessfully(self, review):
        self._addReview(review)
        return AlertSection(self.driver)
        
        
class AddFriendSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = AddFriendSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        
    def enterFirstName(self, friend):
        self.enterText(self.findElement(*self.locator.FIRST_NAME_FIELD), friend.firstName)

    def enterLastName(self, friend):
        self.enterText(self.findElement(*self.locator.LAST_NAME_FIELD), friend.lastName)
        
    def enterEmailAddress(self, friend):
        self.enterText(self.findElement(*self.locator.EMAIL_ADDRESS_FIELD), friend.email)
        
    def pressSave(self):
        self.findElement(*self.locator.SAVE_BUTTON).click()

    def _addFriend(self, friend):
        if friend.firstName:
            self.enterFirstName(friend)
        if friend.lastName:
            self.enterLastName(friend)
        if friend.email:
            self.enterEmailAddress(friend)
        self.pressSave()

    def addFriendSuccessfully(self, friend):
        self._addFriend(friend)
        return MainSection(self.driver)
        
    def addFriendUnsuccessfully(self, friend):
        self._addFriend(friend)
        
    def pressBackArrow(self):
        self.findElement(*self.locator.BACK_ARROW_BUTTON).click()
        return MainSection(self.driver)

        
class FriendEditSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = FriendEditSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        
    def pressUploadPhoto(self):
        self.findElement(*self.locator.UPLOAD_PHOTO_BUTTON).click()

    def enterFirstName(self, friend):
        self.enterText(self.findElement(*self.locator.FIRST_NAME_FIELD), friend.firstName)
        
    def enterLastName(self, friend):
        self.enterText(self.findElement(*self.locator.LAST_NAME_FIELD), friend.lastName)
    
    def enterBirthday(self, friend):
        self.enterText(self.findElement(*self.locator.BIRTHDAY_FIELD), friend.birthday)
    
    def enterEmailAddress(self, friend):
        self.enterText(self.findElement(*self.locator.EMAIL_ADDRESS_FIELD), friend.email)

    def pressHamburger(self):
        self.findElement(*self.locator.HAMBURGER_BUTTON).click()
        
    def pressDelete(self):
        self.findElement(*self.locator.DELETE_BUTTON).click()
        return AlertSection(self.driver)
        
    def pressSave(self):
        self.findElement(*self.locator.SAVE_BUTTON).click()
      
    def deleteFriendSuccessfully(self):
        self.pressHamburger()
        alert = self.pressDelete()
        assert alert.title == "Do you want to delete this friend?"
        alert.pressYes()
        return MainSection(self.driver)
    
    def deleteFriendUnsuccessfully(self):
        self.pressHamburger()
        alert = self.pressDelete()
        assert alert.title == "Do you want to delete this friend?"
        alert.pressNo()
        
    def pressBackArrow(self):
        super().pressBackArrow()
        return FriendSection(self.driver)
        
    def _editFriend(self, friend):
        self.enterFirstName(friend)
        self.enterLastname(friend)
        self.enterEmailAddress(friend)
        #self.enterBirthday(friend.birthday)
        self.pressSave()
        
    def editFriendSuccessfully(self, friend):
        self._editFriend(friend)
        #self.assertToastTextEquals("Friend updated.")
       
    def editFriendUnsuccessfully(self, friend):
       self._editFriend(friend)
       #self.assertToastTextEquals("Failed to update friend.")
        
    @property    
    def emailField(self):
        return self.findElement(*self.locator.EMAIL_ADDRESS_FIELD).text
        
        
class FriendSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = FriendSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
        
    def pressEditFriend(self):
        self.findElement(*self.locator.EDIT_FRIEND_BUTTON).click()
        self._PutAppInBackground()
        return FriendEditSection(self.driver)
        
    def pressBackArrow(self):
        super().pressBackArrow()
        return MainSection(self.driver)
    
    @property
    def friendName(self):
        return self.findElement(*self.locator.FRIEND_NAME_TEXT).text
        
        
class LoggedinUserSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = LoggedinUserSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)
    
    @property
    def whatIWantList(self):
        return FriendItemListSection(self.driver)

    def pressProfileEdit(self, background = True):
        self.findElement(*self.locator.EDIT_PROFILE_BUTTON).click()
        if background:
            self._PutAppInBackground()
        return ProfileSection(self.driver)

    @property
    def username(self):
        return self.findElement(*self.locator.USERNAME_TEXT).text


class EditItemSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = EditItemSectionLocators
        self.activity =  self.locator.ACTIVITY
        super().__init__(driver, **kwargs)

    def enterName(self, item):
        self.enterText(self.findElement(*self.locator.NAME_FIELD), item.itemName)

    def enterPrice(self, item):
        self.enterText(self.findElement(*self.locator.PRICE_FIELD), item.price)

    def enterQuantity(self, item):
        self.enterText(self.findElement(*self.locator.QUANTITY_FIELD), item.qty)

    def enterDescription(self, item):
            self.enterText(self.findElement(*self.locator.DESCRIPTION_FIELD), item.description)

    def pressSave(self):
        self.finElement(*self.locator.SAVE_BUTTON).click()


class ProfileSection(Section):
    def __init__(self, driver, **kwargs):
        self.locator = ProfileSectionLocators
        self.activity = self.locator.ACTIVITY
        super().__init__(driver, **kwargs)

    def enterUsername(self, user):
        self.enterText(self.findElement(*self.locator.USERNAME_FIELD), user.username)

    def enterTagline(self, user):
        self.enterText(self.findElement(*self.locator.TAGLINE_FIELD), user.tagline)

    def enterFirstName(self, user):
        self.enterText(self.findElement(*self.locator.FIRST_NAME_FIELD), user.firstName)

    def enterLastName(self, user):
        self.enterText(self.findElement(*self.locator.LAST_NAME_FIELD), user.lastName)

    def enterWebsite(self, user):
        self.enterText(self.findElement(*self.locator.WEBSITE_FIELD), user.website)

    def enterBio(self, user):
        self.enterText(self.findElement(*self.locator.BIO_FIELD), user.bio)

    def pressSave(self):
        self.findElement(*self.locator.SAVE_BUTTON).click()

    @property
    def username(self):
        return self.findElement(*self.locator.USERNAME_FIELD).text

    @property
    def firstName(self):
        return self.findElement(*self.locator.FIRST_NAME_FIELD).text

    @property
    def lastName(self):
        return self.findElement(*self.locator.LAST_NAME_FIELD).text

    @property
    def tagline(self):
        return self.findElement(*self.locator.TAGLINE_FIELD).text

    @property
    def website(self):
        return self.findElement(*self.locator.WEBSITE_FIELD).text

    @property
    def bio(self):
        return self.findElement(*self.locator.BIO_FIELD).text

    def pressBackArrow(self):
        super().pressBackArrow()
        return LoggedinUserSection(self.driver)