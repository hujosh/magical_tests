import os
from multiprocessing.dummy import Pool
from random import choice
from string import ascii_uppercase

import pytest
from appium import webdriver

from magical.items import Item
from magical.reviews import Review
from magical.users import User
from mobile_app.sections import *
from mobile_app.base import PhoneNetwork

import settings

def assertFriendNotPresent(friend, phone):
    horizontalFriendsListSection = HorizontalFriendsListSection(phone)
    #if horizontalFriendsListSection.friendInList(friend):
     #   raise AssertionError("'%s' should not be in the horizontal friends list but isn't." % friend.fullName)
    verticalFriendsListSection = horizontalFriendsListSection.pressRightArrow()
    if verticalFriendsListSection.friendInList(friend):
        raise AssertionError("'%s' should not be in the vertical friends list but isn't." % friend.fullName)


def assertFriendPresent(friend, phone):
    horizontalFriendsListSection = HorizontalFriendsListSection(phone)
    if not (horizontalFriendsListSection.friendInList(friend)):
        raise AssertionError("'%s' should be in the horizontal friends list, but it isn't." % friend.fullName)
    verticalFriendsListSection = horizontalFriendsListSection.pressRightArrow()
    if not (verticalFriendsListSection.friendInList(friend)):
        raise AssertionError("'%s' should be in the vertical friends list, but it isn't." % friend.fullName)


def assertSectionPresent(section):
    assert section.sectionPresent(), "The app should be in the %s but isn't"%section.getSectionName()


def goBackToMainSection(test, phone):
    test.phone.start_activity(settings.desired_caps['appPackage'], settings.desired_caps['appActivity'])


def getLoggedinUser(pre_defined_user=None):
    user = User(pre_defined_user)
    user.http.createAccount()
    user.http.login()
    return user

def save_screenshot(request):
        directory = os.path.join(os.path.join('%s' % os.path.dirname(os.path.abspath(__file__)),"android_images"),
                                 request.cls.__name__)
        if not(os.path.exists(directory)):
            os.makedirs(directory)
        image_name = request.node.name+".png"
        request.cls.phone.save_screenshot(os.path.join(directory,image_name))

def getRandomString(length):
    return ''.join(choice(ascii_uppercase) for i in range(User.MAX_USERNAME+1))

@pytest.fixture(autouse=True)
def clean(request):
    yield
    if request.node.rep_setup.failed or request.node.rep_call.failed:
        save_screenshot(request)

pytestmark = pytest.mark.usefixtures("clean")


class TestLogin:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(cls, method):
        cls.phone.reset()

    def setup_method(self):
        self.loginSection = LoginSection(TestLogin.phone)

    def test_login_with_extantUser_using_email(self):
        print(self.phone.page_source)
        self.loginSection.loginSuccessfully(User('extantUser'))

    def test_login_with_extantUser_using_username(self):
        self.loginSection.loginSuccessfully(User('extantUser'),withEmail=False)


    def test_login_with_emptyEmail(self):
        alert = self.loginSection.loginUnsuccessfully(User('emptyEmail'))
        if alert.isiOS:
            print(alert.fullAlertText)
            assert alert.fullAlertText == "Error logging in.\nusername is required"
        else:
            assert alert.title == "Username is empty."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_emptyPassword(self):
        alert = self.loginSection.loginUnsuccessfully(User('emptyPassword'))
        if alert.isiOS:
            assert alert.fullAlertText == "Error logging in.\npassword is required"
        else:
            assert alert.title == "Password is empty."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_nonExistentUser(self):
        alert = self.loginSection.loginUnsuccessfully(User('nonExistentUser'))
        if alert.isiOS:
            assert alert.fullAlertText == "Error logging in.\nIncorrect username or password - please try again."
        else:
            assert alert.title == "Error logging in."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_longEmail(self):
        alert = self.loginSection.loginUnsuccessfully(User('longEmail'))
        if alert.isiOS:
            assert alert.fullAlertText == "Error logging in.\nIncorrect username or password - please try again."
        else:
            assert alert.title == "Error logging in."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_emptyEmailAndPassword(self):
        alert = self.loginSection.loginUnsuccessfully(User('emptyEmailAndPassword'))
        if alert.isiOS:
            assert alert.fullAlertText == "Error logging in.\npassword is required"
        else:
            assert alert.title == "Password is empty."
        alert.pressOK()
        assert self.loginSection.sectionPresent()


class TestSignup:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(cls, method):
        cls.phone.reset()

    def setup_method(self):
        self.loginSection = LoginSection(TestSignup.phone)
        self.signupSection = self.loginSection.pressJoinUs()

    def invalid_signup_first_page(self, user, expected_title="Data Invalid",
                                  expected_message="Please ensure all fields are valid."):
        alert = self.signupSection.signupUnsuccessfullyFirstPage(user)
        assert alert.title == expected_title
        if expected_message is not None:
            assert alert.message == expected_message
        alert.pressOK()
        assert self.signupSection.sectionPresent()

    def invalid_signup_second_page(self, user, expected_title="Name Invalid",
                                   expected_message="Please ensure both fields are entered."):
        alert = self.signupSection.signupSuccessfullyFirstPage(user)
        alert.pressConfirm()
        alert = self.signupSection.signupUnsuccessfullySecondPage(user)
        assert alert.title == expected_title
        if expected_message is not None:
            assert alert.message == expected_message

    def test_signup_with_validUser(self):
        # Gets a random user whose data is valid
        user = User()
        # pdb.set_trace()
        alert = self.signupSection.signupSuccessfullyFirstPage(user)
        assert alert.title == "Confirm Email Address"
        assert alert.message == user.email
        alert.pressConfirm()
        alert = self.signupSection.signupSuccessfullySecondPage(user)
        assert alert.title == "Success!"
        assert alert.message == "%s was successfully created. You are now logged in." % user.username
        alert.pressOK()
        mainSection = MainSection(TestSignup.phone)

    
    def test_signup_with_emptyUsername(self):
        self.invalid_signup_first_page(User('emptyUsername'))

    def test_signup_with_usernameTooLong(self):
        self.invalid_signup_first_page(User('usernameTooLong'))

    def test_signup_with_emptyEmail(self):
        self.invalid_signup_first_page(User('emptyEmail'))

    def test_signup_with_emptyPasswords(self):
        self.invalid_signup_first_page(User('emptyPasswords'))

    def test_signup_with_emptyPassword(self):
        self.invalid_signup_first_page(User('emptyPassword'))

    def test_signup_with_emptyRetypedPassword(self):
        self.invalid_signup_first_page(User('emptyRetypedPassword'))

    def test_signup_with_passwordsDontMatch(self):
        self.invalid_signup_first_page(User('passwordsDontMatch'))

    def test_signup_with_emptyFirstName(self):
        self.invalid_signup_second_page(User('emptyFirstName'))

    def test_signup_with_emptyLastName(self):
        self.invalid_signup_second_page(User('emptyLastName'))

    def test_signup_without_accepting_terms_and_conditions(self):
        user = User()
        alert = self.signupSection.signupSuccessfullyFirstPage(user)
        alert.pressConfirm()
        self.signupSection.enterFirstName(user)
        self.signupSection.enterLastName(user)
        self.signupSection.pressSignup()
        alert = AlertSection(TestSignup.phone)
        alert.title = "Terms and Conditions"
        alert.message = "Please review our terms and privacy policy, and check the box"
        alert.pressOK()
        self.signupSection.checkTermsAndConditions()
        self.signupSection.pressSignup()
        alert = AlertSection(TestSignup.phone)
        alert.pressOK()
        assert MainSection().sectionPresent()


class TestForgotPassword:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(cls, method):
        cls.phone.reset()

    def forgot_password(cls, user, expected_message):
        loginSection = LoginSection(cls.phone)
        alert = loginSection.pressForgotPassword()
        alert.enterInput(user.email)
        alert.pressSubmit()
        alert = AlertSection(cls.phone)
        assert alert.title == None
        assert alert.message == expected_message
        alert.pressOK()
        # We should still be in the login section.
        assert loginSection.sectionPresent()

    def test_forgot_passowrd_with_extantUser(self):
        user = User('extantUser')
        alert_message = 'An email has been sent to reset your password.'
        self.forgot_password(user, alert_message)

    def test_forgot_password_with_emptyEmail(self):
        user = User('emptyEmail')
        alert_message = 'Invalid email address.'
        self.forgot_password(user, alert_message)

    def test_forgot_password_with_invalidEmail(self):
        user = User('invalidEmail')
        alert_message = 'Invalid email address.'
        self.forgot_password(user, alert_message)

    def test_forgot_password_with_nonExistentUser(self):
        user = User('nonExistentUser')
        alert_message = 'Sorry - we could not locate email address %s.' % (user.email)
        self.forgot_password(user, alert_message)


class TestAddItem:
    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        user.http.login()
        return user

    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestAddItem.p.imap(cls.create_account, cls.users)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self, method):
        #goBackToMainSection(TestAddItem, TestAddItem.phone)
        TestAddItem.phone.reset()

    def setup_method(self):
        try:
            self.user = TestAddItem.it.next()
            loginSection = LoginSection(TestAddItem.phone)
            TestAddItem.mainSection = loginSection.loginSuccessfully(self.user)
            TestAddItem.mainSection.pressPlus()
            TestAddItem.addItemSection = TestAddItem.mainSection.pressAddItem()
        except:
            self.teardown_method()
            raise

    @pytest.mark.parametrize("item_type", [
        'itemNameHasOnlyNumbers',
        'itemNameContainsOnlyZero',
        'itemNameContainsOnlyNegative1',
        'itemNameHasNumbersAndLetters',
        #'itemNameHasFunnyCharacters'
    ])
    def test_add_item_with_validName(cls, item_type):
        item = Item(item_type)
        cls.addItemSection.addItemSuccessfully(item)
        friendListSection = HorizontalFriendsListSection(cls.phone)
        mySection = friendListSection.pressMe(cls.user)
        mySection.whatIWantList.findItem({'name': item.validatedItemName, 'by': cls.user.internalName})

    @pytest.mark.parametrize("item_type, error_message", [
        ('itemNameIsEmpty', 'A new item must have a name.'),
        ('itemNameContainsOnlyASpace', 'A new item must have a name.')
    ])
    def test_add_item_with_invalidName(cls, item_type, error_message):
        item = Item(item_type)
        alert = cls.addItemSection.addItemUnsuccessfully(item)
        assert alert.message == error_message
        alert.pressOK()
        assert cls.addItemSection.sectionPresent()

    @pytest.mark.parametrize("item_type", [
        'priceIsNegative',
        'priceHasLetters',
        'priceTooLarge',
        'priceHas3DecimalPlaces',
    ])
    def test_add_item_with_invalidPrice(cls, item_type):
        item = Item(item_type)
        cls.addItemSection.addItemSuccessfully(item)
        friendListSection = HorizontalFriendsListSection(cls.phone)
        mySection = friendListSection.pressMe(cls.user)
        viewItemSection = mySection.whatIWantList.pressItem(
            {'name': item.validatedItemName, 'by': cls.user.internalName})
        assert viewItemSection.price == item.validatedItemPrice

    @pytest.mark.parametrize("item_type", [
        "priceIsEmpty",
        "priceIsZero",
    ])
    def test_add_item_with_validPrice(cls, item_type):
        item = Item(item_type)
        cls.addItemSection.addItemSuccessfully(item)
        friendListSection = HorizontalFriendsListSection(cls.phone)
        mySection = friendListSection.pressMe(cls.user)
        viewItemSection = mySection.whatIWantList.pressItem(
            {'name': item.validatedItemName, 'by': cls.user.internalName})
        assert viewItemSection.price == item.validatedItemPrice

    '''
    def test_add_item_with_anyoneCanKnow(self):
        pass

    def test_add_item_with_friendsCanKnow(self):
        pass

    def test_add_item_with_onlyMeCanKnow(self):
        pass

    def test_add_item_with_occasion(self):
        pass
    '''


class TestLogout:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(cls):
        cls.phone.reset()

    def test_logout(cls):
        loginSection = LoginSection(cls.phone)
        mainSection = loginSection.loginSuccessfully(User('extantUser'))
        settingsSection = mainSection.pressSettingsButton()
        settingsSection.pressLogoutButton()
        alert = AlertSection(cls.phone)
        assert alert.message == 'Are you sure you want to log out?'
        alert.pressYes()
        assert loginSection.sectionPresent()


class TestReview:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)
        cls.user = User()
        cls.user.http.createAccount()
        cls.user.http.login()
        cls.item = Item()
        cls.user.http.addItem(cls.item)
        loginSection = LoginSection(cls.phone)
        cls.mainSection = loginSection.loginSuccessfully(cls.user)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        goBackToMainSection(TestReview, TestReview.phone)

    @pytest.mark.parametrize("review_type, error_message", [
        ("emptyReviewText", "Comment is required."),
    ])
    def test_add_invalidReview(cls, review_type, error_message):
        friendListSection = HorizontalFriendsListSection(cls.phone)
        mySection = friendListSection.pressMe(cls.user)
        viewItemSection = mySection.whatIWantList.pressItem({'name': cls.item.itemName, 'by': cls.user.internalName})
        viewItemSection.flick('down')
        reviewSection = viewItemSection.pressAddReviewButton()
        alert = reviewSection.addReviewUnsuccessfully(Review(review_type))
        assert alert.title == error_message
        alert.pressOK()
        assert reviewSection.sectionPresent()

    @pytest.mark.parametrize("review_type", [
        "zeroStarReview",
        "oneStarReview",
        "twoStarReview",
        "threeStarReview",
        "fourStarReview",
        "fiveStarReview",
    ])
    def test_add_validReview(cls, review_type):
        friendListSection = HorizontalFriendsListSection(cls.phone)
        mySection = friendListSection.pressMe(cls.user)
        viewItemSection = mySection.whatIWantList.pressItem({'name': cls.item.itemName, 'by': cls.user.internalName})
        viewItemSection.flick('down')
        reviewSection = viewItemSection.pressAddReviewButton()
        review = Review(review_type)
        editeItemSection = reviewSection.addReviewSuccessfully(review)
        assert viewItemSection.reviewList.reviewInList(review)

        # def test_edit_review(cls):
        #    pass

        # def test_delete_review(cls):
        #    pass

class TestAddFriend:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)
        cls.user = User()
        cls.user.http.createAccount()
        loginSection = LoginSection(cls.phone)
        cls.mainSection = loginSection.loginSuccessfully(cls.user)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        # go back to MainSection...
        TestAddFriend.phone.start_activity(settings.desired_caps['appPackage'], settings.desired_caps['appActivity'])

    def setup_method(self):
        try:
            TestAddFriend.mainSection.pressPlus()
            self.user = TestAddFriend.user
            self.addFriendSection = self.mainSection.pressAddFriend()
        except:
            self.teardown_method()
            raise

    @pytest.mark.parametrize("friend_type", [
        "emptyName",
        "invalidEmail",
    ])
    def test_add_invalidFriend(self, friend_type):
        friend = User(friend_type)
        self.addFriendSection.addFriendUnsuccessfully(friend)
        # We should still be in the addFriendSection
        assert self.addFriendSection.sectionPresent()
        self.addFriendSection.pressBackArrow()
        assertFriendNotPresent(friend, TestAddFriend.phone)

    def test_add_friend_whose_email_is_same_as_logged_in_users(self):
        friend = User()
        friend.email = self.user.email
        self.addFriendSection.addFriendUnsuccessfully(friend)
        # We should still be in the addFriendSection
        assert self.addFriendSection.sectionPresent()
        self.addFriendSection.pressBackArrow()
        assertFriendNotPresent(friend, TestAddFriend.phone)

    @pytest.mark.parametrize("friend_type", [
        "emptyLastName",
        "emptyEmail",
        "emptyLastNameEmptyEmail",
        # A friend whose details are random...
        'random',
        #'funnyCharInFirstName',
        #'funnyCharInLastName',
    ])
    def test_add_valid_non_magical_friend(self, friend_type):
        friend = User(friend_type)
        mainSection = self.addFriendSection.addFriendSuccessfully(friend)
        assertFriendPresent(friend, TestAddFriend.phone)

    def test_add_valid_magical_friend(self):
        friend = User()
        friend.http.createAccount()
        mainSection = self.addFriendSection.addFriendSuccessfully(friend)
        assertFriendPresent(friend, TestAddFriend.phone)

    def test_add_friend_whose_email_same_as_current_friends(self):
        friend = User()
        friend.http.createAccount()
        self.user.http.login()
        friend2 = User()
        friend2.email = friend.email
        self.user.http.addFriend(friend)
        self.addFriendSection.addFriendUnsuccessfully(friend2)
        assert self.addFriendSection.sectionPresent()
        self.addFriendSection.pressBackArrow()
        assertFriendNotPresent(friend2, TestAddFriend.phone)


class TestFriendEdit:
    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        user.http.login()
        friend = User()
        user.http.addFriend(friend)
        return user, friend

    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestFriendEdit.p.imap(cls.create_account, cls.users)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        #goBackToMainSection(TestFriendEdit, TestFriendEdit.phone)
        TestFriendEdit.phone.reset()

    def setup_method(self):
        try:
            self.user, self.friend = TestFriendEdit.it.next()
            loginSection = LoginSection(TestFriendEdit.phone)
            loginSection.loginSuccessfully(self.user)
            horFriendList = HorizontalFriendsListSection(TestFriendEdit.phone)
            verFriendList = horFriendList.pressRightArrow()
            friendSection = verFriendList.pressFriend(self.friend)
            self.friendProfile = friendSection.pressEditFriend()
        except:
            self.teardown_method()
            raise

    '''
    @pytest.mark.parametrize("invalid_name", [
        "",  # empty name
        "$", # invalid character
        ' ' #space
    ])
    def test_invalid_name_change(self, invalid_name):
        old_name = self.friend.fullName
        self.friend.fullName = invalid_name
        self.friendProfile.enterName(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        # assert that the name wasn't changed
        assert friendSection.friendName == old_name

    @pytest.mark.parametrize("valid_name", [
        'NEW'
    ])
    def test_valid_name_change(self, valid_name):
        self.friend.setFirstName(valid_name)
        self.friendProfile.enterName(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        assert friendSection.friendName == self.friend.fullName
        friendSection.pressBackArrow()

        assertFriendPresent(self.friend)

    '''
    def test_change_email_to_same_as_loggedin_users(self):
        old_email = self.friend.email
        self.friend.email = self.user.email
        self.friendProfile.enterEmailAddress(self.friend)
        self.friendProfile = self.friendProfile.pressSaveUnsuccessful()
        #assert self.friendProfile.emailField == old_email
        friendSection = self.friendProfile.pressBackArrow()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == old_email

    def test_change_email_to_blank(self):
        old_email = self.friend.email
        self.friend.email = ''
        self.friendProfile.enterEmailAddress(self.friend)
        friendSection = self.friendProfile.pressSaveSuccessful()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == self.friend.email

    def test_change_email_to_random_valid_email(self):
        old_email = self.friend.email
        self.friend.email = 'a' + self.friend.email
        self.friendProfile.enterEmailAddress(self.friend)
        friendSection = self.friendProfile.pressSaveSuccessful()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == self.friend.email

    def test_change_email_to_that_of_extant_friend(self):
        # create a new friend...
        friend2 = User()
        self.user.http.addFriend(friend2)
        old_email = self.friend.email
        self.friend.email = friend2.email
        self.friendProfile.enterEmailAddress(self.friend)
        self.friendProfile = self.friendProfile.pressSaveUnsuccessful()
        #assert self.friendProfile.emailField == old_email
        friendSection = self.friendProfile.pressBackArrow()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == old_email


class TestDeleteFriend:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        TestDeleteFriend.phone.reset()

    def setup_method(self):
        try:
            self.user = getLoggedinUser()
            self.friend = User()
            self.user.http.addFriend(self.friend)
            loginSection = LoginSection(TestDeleteFriend.phone)
            mainSection = loginSection.loginSuccessfully(self.user)
            horizontalFriendsList = HorizontalFriendsListSection(TestDeleteFriend.phone)
            self.friendSection = horizontalFriendsList.pressFriend(self.friend)
            self.editFriendSection = self.friendSection.pressEditFriend()
        except:
            self.teardown_method()
            raise

    def test_delete_non_magical_friend(self):
        mainSection = self.editFriendSection.deleteFriendSuccessfully()
        assertFriendNotPresent(self.friend, TestDeleteFriend.phone)

    def test_do_not_delete_non_magical_friend(self):
        self.editFriendSection.deleteFriendUnsuccessfully()
        assert self.editFriendSection.sectionPresent()
        friendSection = self.editFriendSection.pressBackArrow()
        mainSection = friendSection.pressBackArrow()
        assertFriendPresent(self.friend, TestDeleteFriend.phone)


class TestEditItem():
    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        user.http.login()
        item = Item()
        user.http.addItem(item)
        return user,item

    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestEditItem.p.imap(cls.create_account, cls.users)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        #goBackToMainSection(TestEditItem, TestEditItem.phone)
        TestEditItem.phone.reset()

    def setup_method(self):
        self.user, self.item = TestEditItem.it.next()
        loginSection = LoginSection(TestEditItem.phone)
        loginSection.loginSuccessfully(self.user)
        horFriendList = HorizontalFriendsListSection(TestEditItem.phone)
        mySection = horFriendList.pressMe(self.user)
        itemSection = mySection.whatIWantList.pressItem({'name': self.item.validatedItemName, 'by': self.user.internalName})
        self.editItemSection = itemSection.pressEditItem()

    @pytest.mark.parametrize("name", [
        'NEW',
    ])
    def test_valid_name_change(self, name):
        self.item.itemName = name
        self.editItemSection.enterName(self.item)
        item_page = self.editItemSection.pressSaveSuccessfully()
        assert item_page.itemName == self.item.itemName

    @pytest.mark.parametrize("name", [
        ' ', # space
        '', # empty
    ])
    def test_invalid_name_change(self, name):
        old_name = self.item.itemName
        self.item.itemName = name
        self.editItemSection.enterName(self.item)
        alert = self.editItemSection.pressSaveUnsuccessfully()
        assert alert.title == "Invalid field"
        assert alert.message == "Item must have a name."
        alert.pressOK()
        assert self.editItemSection.sectionPresent()
        item_page = self.editItemSection.pressBackArrow()
        assert item_page.itemName == old_name


class TestProfile:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        goBackToMainSection(TestProfile, TestProfile.phone)

    def setup_method(self):
        self.user = User()
        self.user.http.createAccount()
        loginSection = LoginSection(TestProfile.phone)
        loginSection.loginSuccessfully(self.user)
        friendList = HorizontalFriendsListSection(TestProfile.phone)
        mySection = friendList.pressMe(self.user)
        self.myProfile = mySection.pressProfileEdit()

    def testProfileDataCorrect(self):
        '''Tests that the data in the profile upon logging in for the first time is correct'''
        print(self.myProfile.driver.page_source)
        assert self.myProfile.username == self.user.username
        assert self.myProfile.firstName == self.user.firstName
        assert self.myProfile.lastName == self.user.lastName
        # The remaining fields of the profile should be blank, because they have not yet been set.
        assert self.myProfile.tagline == ""
        assert self.myProfile.website == ""
        assert self.myProfile.bio == ""


class TestProfileEdit:
    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        return user

    @classmethod
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestProfileEdit.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        #goBackToMainSection(TestProfileEdit, TestProfileEdit.phone)
        TestProfileEdit.phone.reset()

    def setup_method(self):
        try:
            self.user = TestProfileEdit.it.next()
            loginSection = LoginSection(TestProfileEdit.phone)
            loginSection.loginSuccessfully(self.user)
            friendList = HorizontalFriendsListSection(TestProfileEdit.phone)
            mySection = friendList.pressMe(self.user)
            self.myProfile = mySection.pressProfileEdit()
        except:
            self.teardown_method()
            raise

    @pytest.mark.parametrize("name", [
        '' # you can't have an empty name
    ])
    def test_first_name_invalid(self, name):
        old_name = self.myProfile.firstName
        self.user.setFirstName(name)
        self.myProfile.enterFirstName(self.user)
        mySection = self.myProfile.pressSave()
        #mySection = self.myProfile.pressBackArrow()
        myProfile = mySection.pressProfileEdit()
        assert myProfile.firstName == old_name

    @pytest.mark.parametrize("name", [
        'Greg',
        #'Pökémön'
    ])
    def test_first_name_valid(self, name):
        self.user.setFirstName(name)
        self.myProfile.enterFirstName(self.user)
        mySection = self.myProfile.pressSave()
        #mySection = self.myProfile.pressBackArrow()
        myProfile = mySection.pressProfileEdit()
        assert myProfile.firstName == self.user.firstName

    @pytest.mark.parametrize("name", [
        getRandomString(User.MAX_USERNAME+1),
        '%' + getRandomString(User.MAX_USERNAME ), # invalid char %
        '', #empty username
        ' ' # space in username
    ])
    def test_username_invalid(self, name):
        old_username = self.myProfile.username
        self.user.username = name
        self.myProfile.enterUsername(self.user)
        mySection = self.myProfile.pressSave()
        #mySection = self.myProfile.pressBackArrow()
        assert mySection.username == old_username
        myProfile = mySection.pressProfileEdit()
        assert myProfile.username == old_username

    def test_username_already_exists(self):
        other_user = User()
        other_user.http.createAccount()
        old_username = self.myProfile.username
        self.user.username = other_user.username
        self.myProfile.enterUsername(self.user)
        mySection = self.myProfile.pressSave()
        #mySection = self.myProfile.pressBackArrow()
        assert mySection.username == old_username
        myProfile = mySection.pressProfileEdit()
        assert myProfile.username == old_username

    '''
    def test_username_valid(self):
        pass

    def test_last_name_invalid(self):
        pass

    def test_last_name_valid(self):
        pass

    def test_website_invalid(self):
        pass

    def test_website_valid(self):
        pass

    def test_bio_valid(self):
        pass

    def test_bio_invalid(self):
        pass

    def test_change_privacy(self):
        pass'''


class TestLikeItem:
    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        user.http.login()
        item = Item()
        user.http.addItem(item)
        return user, item

    @classmethod
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestLikeItem.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        # goBackToMainSection(TestProfileEdit, TestProfileEdit.phone)
        TestLikeItem.phone.reset()

    def setup_method(self):
        self.user, self.item = TestLikeItem.it.next()
        loginSection = LoginSection(TestLikeItem.phone)
        loginSection.loginSuccessfully(self.user)

    def test_like_my_item(self):
        friends_list = HorizontalFriendsListSection(TestLikeItem.phone)
        mySection = friends_list.pressMe(self.user)
        mySection.whatIWantList.pressLikeItem({'name':self.item.itemName, 'by':self.user.internalName})
        assert mySection.whatIWantList.itemLikeCount({'name':self.item.itemName, 'by':self.user.internalName}) == 1
        mySection.whatIWantList.pressLikeItem({'name':self.item.itemName, 'by':self.user.internalName})
        assert mySection.whatIWantList.itemLikeCount({'name':self.item.itemName, 'by':self.user.internalName}) == 0
        mySection.whatIWantList.pressLikeItem({'name': self.item.itemName, 'by': self.user.internalName})
        assert mySection.whatIWantList.itemLikeCount({'name':self.item.itemName, 'by':self.user.internalName}) == 1
        item_page = mySection.whatIWantList.pressItem({'name': self.item.itemName, 'by': self.user.internalName})
        assert item_page.likeCount == 1
        item_page.pressLikeButton()
        assert item_page.likeCount == 0
        item_page.pressBackArrow()
        my_section = LoggedinUserSection(TestLikeItem.phone)
        assert mySection.whatIWantList.itemLikeCount({'name':self.item.itemName, 'by':self.user.internalName}) == 0


class TestDeleteItem:
    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        user.http.login()
        item = Item()
        user.http.addItem(item)
        return user, item

    @classmethod
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestDeleteItem.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        # goBackToMainSection(TestProfileEdit, TestProfileEdit.phone)
        TestDeleteItem.phone.reset()

    def setup_method(self):
        self.user, self.item = TestDeleteItem.it.next()
        loginSection = LoginSection(TestDeleteItem.phone)
        loginSection.loginSuccessfully(self.user)

    def test_delete_my_item(self):
        friendList = HorizontalFriendsListSection(TestDeleteItem.phone)
        myPage = friendList.pressMe(self.user)
        item_page =  myPage.whatIWantList.pressItem({'name': self.item.itemName, 'by': self.user.internalName})
        myPage = item_page.deleteItem()
        assert myPage.whatIWantList.itemInList({'name': self.item.itemName, 'by': self.user.internalName}) == False


    def test_delete_friends_item(self):
        me = User("extantuser")
        friend = User("davidGoddard")
        friend.http.login()
        item = Item()
        friend.http.addItem(item)
        self.user.http.addFriend(friend)
        time.sleep(5)
        horFriendList = HorizontalFriendsListSection(TestDeleteItem.phone)
        verFriendList = horFriendList.pressRightArrow()
        friendSection = verFriendList.pressFriend(friend)
        item_page = friendSection.whatMyFriendWantsList.pressItem({'name': item.itemName, 'by': friend})
        with pytest.raises(ElementNotFound) as excinfo:
            item_page.pressHamburer() # Trying to press the hamburger should raise an exception...


class TestOfflineMode:
    @classmethod
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestOfflineMode.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)
        cls.phoneNetwork = PhoneNetwork()

    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        return user

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        # goBackToMainSection(TestProfileEdit, TestProfileEdit.phone)
        TestOfflineMode.phoneNetwork.set_network_connection("enable")
        TestOfflineMode.phone.reset()

    def setup_method(self):
        self.user = TestOfflineMode.it.next()


    def test_disconnect_before_login(self):
        '''
            A user's phone disconnects, the user logs in (and fails) and then his phone
            reconnects and he logs in (successfully).
        '''

        TestOfflineMode.phoneNetwork.set_network_connection("disable")
        loginSection = LoginSection(TestOfflineMode.phone)
        alert = loginSection.loginUnsuccessfully(self.user)
        assert alert.title == "Error logging in."
        alert.pressOK()
        TestOfflineMode.phoneNetwork.set_network_connection("enable")
        time.sleep(5) # Wait for the connection to re-establish
        loginSection.pressLogin()
        assert MainSection(TestOfflineMode.phone).sectionPresent()
    
    def test_losing_connection(self):
        '''
            A user is logged in, leaves the app (without logging out), looses
            connection, and then re-opens the app.
            He should still be logged in (in off-line mode).
        '''
        loginSection = LoginSection(TestOfflineMode.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        TestOfflineMode.phoneNetwork.set_network_connection("disable")
        loginSection._PutAppInBackground(5)
        assert mainSection.sectionPresent()

    
    def test_add_item_without_connection(self):
        '''
        The item should appear in the unsynced items section.
        '''
        loginSection = LoginSection(TestOfflineMode.phone)
        mainSection=loginSection.loginSuccessfully(self.user)
        TestOfflineMode.phoneNetwork.set_network_connection("disable")
        mainSection.pressPlus()
        addItemSection = mainSection.pressAddItem()
        item = Item()
        mainSection = addItemSection.addItemSuccessfully(item)
        settingsSection = mainSection.pressSettingsButton()
        unsyncedItemsSection = settingsSection.pressUnsyncedItemsButton()
        assert unsyncedItemsSection.itemInList(item.itemName)

    '''    
    def test_add_friend_without_connection(self):
        pass
    '''

    '''
    def test_edit_item_without_connection(self):
        pass
    '''

@pytest.mark.skip(reason="rotation has been disabled in the Android app.")
class TestRotation:
    @classmethod
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestRotation.p.imap(cls.create_account, cls.users)

    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        return user

    def teardown_method(self):
        TestRotation.phone.orientation = "PORTRAIT"
        TestRotation.phone.quit()

    def setup_method(self):
        TestRotation.phone = webdriver.Remote(settings.host, settings.desired_caps)
        self.user = TestRotation.it.next()

    def toggle_rotation(self):
        TestRotation.phone.orientation = "LANDSCAPE"

    def test_rotation_login_section(self):
        self.toggle_rotation()
        time.sleep(3)
        loginSection = LoginSection(TestRotation.phone)
        assert loginSection.sectionPresent()

    def test_rotation_main_section(self):
        print (TestRotation.phone.orientation)

        loginSection = LoginSection(TestRotation.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        self.toggle_rotation()
        time.sleep(3)
        assert mainSection.sectionPresent()

    
    def test_rotation_add_item_section(self):
        loginSection = LoginSection(TestRotation.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        mainSection.pressPlus()
        addItemSection = mainSection.pressAddItem()
        self.toggle_rotation()
        time.sleep(3)
        assert addItemSection.sectionPresent()

    def  test_rotation_add_friend_section(self):
        loginSection = LoginSection(TestRotation.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        mainSection.pressPlus()
        sddFriendSection = mainSection.pressAddFriend()
        self.toggle_rotation()
        time.sleep(3)
        assert sddFriendSection.sectionPresent()

    def test_rotation_logged_in_users_sectuion(self):
        loginSection = LoginSection(TestRotation.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        friends_list = HorizontalFriendsListSection(TestRotation.phone)
        mySection = friends_list.pressMe(self.user)
        self.toggle_rotation()
        time.sleep(3)
        assert mySection.sectionPresent()


    #def test_rotation_friends_section(self):

class TestChangePassword():
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestChangePassword.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        return user

    def teardown_method(self):
        TestChangePassword.phone.reset()

    def setup_method(self):
        self.user = TestChangePassword.it.next()
        loginSection = LoginSection(TestChangePassword.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        self.changePasswordSection = ChangePasswordSection.goTo(TestChangePassword.phone)


    def test_change_password_withNewPasswordNotTheSame(self):
        new_password = "abc123"
        different_new_password = new_password +"a"
        self.changePasswordSection.enterOriginalPassword(self.user.password)
        self.changePasswordSection.enterNewPassword(new_password)
        self.changePasswordSection.enterConfirmPassword(different_new_password)# Different new passwords
        self.changePasswordSection.pressSaveButton()
        settingsSection = self.changePasswordSection.pressBackArrow().pressBackArrow()
        loginSection = settingsSection.logOut()
        old_password = self.user.password
        self.user.password = new_password
        alert = loginSection.loginUnsuccessfully(self.user)  # Password is wrong
        alert.pressOK()
        self.user.password = different_new_password
        alert = loginSection.loginUnsuccessfully(self.user,clear=True)  # Password is wrong
        alert.pressOK()
        self.user.password = old_password
        mainSection = loginSection.loginSuccessfully(self.user, clear=True)  # Password is right

    def test_change_password_with_wrongOldPassword(self):
        incorrect_original_password = self.user.password+"a"
        new_password = "abc123"
        self.changePasswordSection.enterOriginalPassword(incorrect_original_password)
        self.changePasswordSection.enterNewPassword(new_password)
        self.changePasswordSection.enterConfirmPassword(new_password)
        self.changePasswordSection.pressSaveButton()
        settingsSection = self.changePasswordSection.pressBackArrow().pressBackArrow()
        loginSection = settingsSection.logOut()
        old_password = self.user.password
        self.user.password = incorrect_original_password
        alert = loginSection.loginUnsuccessfully(self.user)  # Password is wrong
        alert.pressOK()
        self.user.password = old_password
        loginSection.loginSuccessfully(self.user, clear=True)

    def test_change_password_with_ValidInput(self):
        new_password = "abc123"
        self.changePasswordSection.enterOriginalPassword(self.user.password)
        self.changePasswordSection.enterNewPassword(new_password)
        self.changePasswordSection.enterConfirmPassword(new_password)
        self.changePasswordSection.pressSaveButton()
        #self.changePasswordSection.assertToastTextEquals("POO")
        settingsSection = self.changePasswordSection.pressBackArrow().pressBackArrow()
        loginSection = settingsSection.logOut()
        alert = loginSection.loginUnsuccessfully(self.user) # Password is wrong
        alert.pressOK()
        self.user.password = new_password
        loginSection.loginSuccessfully(self.user, clear=True)

    def test_change_password_with_invalidNewPasswords(self):
        invalid_new_password = "a"
        self.changePasswordSection.enterOriginalPassword(self.user.password)
        self.changePasswordSection.enterNewPassword(invalid_new_password)
        self.changePasswordSection.enterConfirmPassword(invalid_new_password)
        self.changePasswordSection.pressSaveButton()
        settingsSection = self.changePasswordSection.pressBackArrow().pressBackArrow()
        loginSection = settingsSection.logOut()
        old_password = self.user.password
        self.user.password = invalid_new_password
        alert = loginSection.loginUnsuccessfully(self.user)  # Password is wrong
        alert.pressOK()
        self.user.password = old_password
        loginSection.loginSuccessfully(self.user, clear=True)

'''
class TestAddEvent():
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestAddEvent.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        return user

    def teardown_method(self):
        TestAddEvent.phone.reset()

    def setup_method(self):
        self.user = TestAddEvent.it.next()
        loginSection = LoginSection(TestAddEvent.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        self.calendarSection = mainSection.pressToggleCalendarButton()

    def test_add_event(self):
        self.calendarSection.pressDay(23)
'''

class TestQuickAddFriends():
    def setup_class(cls):
        cls.users = [User() for i in range(15)]
        cls.p = Pool(15)
        cls.it = TestQuickAddFriends.p.imap(cls.create_account, cls.users)
        cls.phone = webdriver.Remote(settings.host, settings.desired_caps)

    @classmethod
    def create_account(cls, user):
        user.http.createAccount()
        return user

    def teardown_method(self):
        TestQuickAddFriends.phone.reset()

    def setup_method(self):
        self.user = TestQuickAddFriends.it.next()
        loginSection = LoginSection(TestChangePassword.phone)
        mainSection = loginSection.loginSuccessfully(self.user)
        self.quickAddFriendSection = QuickAddFriendsSection.goTo(TestQuickAddFriends.phone)

    @pytest.mark.parametrize("name", [
        '',  # empty username
        ' '  # space in username
    ])
    def test_add_friend_invalidName(self, name):
        self.quickAddFriendSection.entername(name)
        self.quickAddFriendSection.pressAddButton()
        self.quickAddFriendSection.assertControlPresent(QuickAddFriendsSectionLocators.EDIT_BUTTON)

