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

host = 'http://localhost:4723/wd/hub'
# Information about the phone; all tests use this dictionary...
desired_caps = {}
desired_caps['deviceName'] = 'D1AGAS3770501528'
# Returns abs path relative to this file and not cwd
desired_caps['app'] = os.path.abspath(r'apps\delayedaddbuild.apk')
desired_caps['appPackage'] = 'magicalconnect.android.magical.dev'
desired_caps['appActivity'] = 'com.android.magical.Presentation.SplashScreen.SplashScreenActivity'
desired_caps['browserName'] = ""
desired_caps['appiumVersion'] = "1.7.1"
desired_caps['deviceOrientation'] = "portrait"
desired_caps['platformName'] = "Android"
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"]= True
desired_caps["automationName "]= 'uiautomator2'


def assertFriendNotPresent(friend, phone):
    horizontalFriendsListSection = HorizontalFriendsListSection(phone)
    if horizontalFriendsListSection.friendInList(friend):
        raise AssertionError("'%s' should not be in the horizontal friends list but isn't." % friend.fullName)
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

def goBackToMainSection(test, phone):
    test.phone.start_activity(desired_caps['appPackage'], desired_caps['appActivity'])


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
        cls.phone = webdriver.Remote(host, desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(cls, method):
        cls.phone.reset()

    def setup_method(self):
        self.loginSection = LoginSection(TestLogin.phone)

    def test_login_with_extantUser_using_email(self):
        self.loginSection.loginSuccessfully(User('extantUser'))

    def test_login_with_extantUser_using_username(self):
        self.loginSection.loginSuccessfully(User('extantUser'),withEmail=False)

    def test_login_with_emptyEmail(self):
        alert = self.loginSection.loginUnsuccessfully(User('emptyEmail'))
        assert alert.title == "Username is empty."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_emptyPassword(self):
        alert = self.loginSection.loginUnsuccessfully(User('emptyPassword'))
        assert alert.title == "Password is empty."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_nonExistentUser(self):
        alert = self.loginSection.loginUnsuccessfully(User('nonExistentUser'))
        assert alert.title == "Error logging in."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_longEmail(self):
        alert = self.loginSection.loginUnsuccessfully(User('longEmail'))
        assert alert.title == "Error logging in."
        alert.pressOK()
        assert self.loginSection.sectionPresent()

    def test_login_with_emptyEmailAndPassword(self):
        alert = self.loginSection.loginUnsuccessfully(User('emptyEmailAndPassword'))
        assert alert.title == "Username is empty."
        alert.pressOK()
        assert self.loginSection.sectionPresent()


class TestSignup:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(host, desired_caps)

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


class TestForgotPassword:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(host, desired_caps)

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
        cls.phone = webdriver.Remote(host, desired_caps)
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
        self.user = TestAddItem.it.next()
        loginSection = LoginSection(TestAddItem.phone)
        TestAddItem.mainSection = loginSection.loginSuccessfully(self.user)
        TestAddItem.mainSection.pressPlus()
        TestAddItem.addItemSection = TestAddItem.mainSection.pressAddItem()

    @pytest.mark.parametrize("item_type", [
        'itemNameHasOnlyNumbers',
        'itemNameContainsOnlyZero',
        'itemNameContainsOnlyNegative1',
        'itemNameHasNumbersAndLetters',
        'itemNameHasFunnyCharacters'
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
        cls.phone = webdriver.Remote(host, desired_caps)

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
        cls.phone = webdriver.Remote(host, desired_caps)
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
        cls.phone = webdriver.Remote(host, desired_caps)
        cls.user = User()
        cls.user.http.createAccount()
        loginSection = LoginSection(cls.phone)
        cls.mainSection = loginSection.loginSuccessfully(cls.user)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        # go back to MainSection...
        TestAddFriend.phone.start_activity(desired_caps['appPackage'],desired_caps['appActivity'])

    def setup_method(self):
        TestAddFriend.mainSection.pressPlus()
        self.user = TestAddFriend.user
        self.addFriendSection = self.mainSection.pressAddFriend()

    @pytest.mark.parametrize("friend_type", [
        "emptyFirstName",
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
        'funnyCharInFirstName',
        'funnyCharInLastName',
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
        cls.phone = webdriver.Remote(host, desired_caps)
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

    @pytest.mark.parametrize("invalid_name", [
        "",  # empty name
        "$", # invalid character
        ' ' #space
    ])
    def test_invalid_first_name_change(self, invalid_name):
        old_name = self.friend.fullName
        self.friend.setFirstName(invalid_name, shouldTrim = False)
        self.friendProfile.enterFirstName(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        # assert that the name wasn't changed
        assert friendSection.friendName == old_name

    @pytest.mark.parametrize("valid_name", [
        'NEW'
    ])
    def test_valid_first_name_change(self, valid_name):
        self.friend.setFirstName(valid_name)
        self.friendProfile.enterFirstName(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        assert friendSection.friendName == self.friend.fullName
        friendSection.pressBackArrow()
        assertFriendPresent(self.friend)

    @pytest.mark.parametrize("valid_name", [
        'NEW'
    ])
    def test_valid_last_name_change(self, valid_name):
        self.friend.setLastName(valid_name)
        self.friendProfile.enterLastName(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        assert friendSection.friendName == self.friend.fullName
        friendSection.pressBackArrow()
        assertFriendPresent(self.friend)

    @pytest.mark.parametrize("invalid_name", [
        '$'
    ])
    def test_invalid_last_name_change(self, invalid_name):
        old_name = self.friend.fullName
        self.friend.setLastName(invalid_name)
        self.friendProfile.enterLastName(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        # assert that the name wasn't changed
        assert friendSection.friendName == old_name

    def test_change_email_to_same_as_loggedin_users(self):
        old_email = self.friend.email
        self.friend.email = self.user.email
        self.friendProfile.enterEmailAddress(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == old_email

    def test_change_email_to_blank(self):
        old_email = self.friend.email
        self.friend.email = ''
        self.friendProfile.enterEmailAddress(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == self.friend.email

    def test_change_email_to_random_valid_email(self):
        old_email = self.friend.email
        self.friend.email = 'a' + self.friend.email
        self.friendProfile.enterEmailAddress(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == self.friend.email

    def test_change_email_to_that_of_extant_friend(self):
        # create a new friend...
        friend2 = User()
        self.user.http.addFriend(friend2)
        old_email = self.friend.email
        self.friend.email = friend2.email
        self.friendProfile.enterEmailAddress(self.friend)
        self.friendProfile.pressSave()
        assert self.friendProfile.sectionPresent()
        friendSection = self.friendProfile.pressBackArrow()
        friendProfile = friendSection.pressEditFriend()
        assert friendProfile.emailField == old_email


class TestDeleteFriend:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(host, desired_caps)

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
    def setup_class(cls):
        cls.phone = webdriver.Remote(host, desired_caps)
        cls.user = User()
        cls.user.http.createAccount()
        cls.user.http.login()
        loginSection = LoginSection(cls.phone)
        loginSection.loginSuccessfully(cls.user)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        goBackToMainSection(TestEditItem, TestEditItem.phone)

    def setup_method(self):
        self.user = TestEditItem.user
        self.item = Item()
        self.user.http.addItem(self.item)
        horFriendList = HorizontalFriendsListSection(TestEditItem.phone)
        mySection = horFriendList.pressMe(self.user)
        itemSection = mySection.whatIWantList.pressItem({'name': self.item.validatedItemName, 'by': self.user.internalName})
        self.editItemSection = itemSection.pressEditItem()

    def test_valid_name_change(self):
        old_name = self.item.itemName
        self.item.itemName = "poo"
        self.editItemSection.enterName(self.item)
        self.editItemSection.pressSave()

class TestProfile:
    @classmethod
    def setup_class(cls):
        cls.phone = webdriver.Remote(host, desired_caps)

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
        cls.phone = webdriver.Remote(host, desired_caps)

    @classmethod
    def teardown_class(cls):
        cls.phone.quit()

    def teardown_method(self):
        #goBackToMainSection(TestProfileEdit, TestProfileEdit.phone)
        TestProfileEdit.phone.reset()

    def setup_method(self):
        self.user = TestProfileEdit.it.next()
        loginSection = LoginSection(TestProfileEdit.phone)
        loginSection.loginSuccessfully(self.user)
        friendList = HorizontalFriendsListSection(TestProfileEdit.phone)
        mySection = friendList.pressMe(self.user)
        self.myProfile = mySection.pressProfileEdit()

    @pytest.mark.parametrize("name", [
        '' # you can't have an empty name
    ])
    def test_first_name_invalid(self, name):
        old_name = self.myProfile.firstName
        self.user.setFirstName(name)
        self.myProfile.enterFirstName(self.user)
        self.myProfile.pressSave()
        mySection = self.myProfile.pressBackArrow()
        myProfile = mySection.pressProfileEdit()
        assert myProfile.firstName == old_name

    @pytest.mark.parametrize("name", [
        'Greg',
        'Pökémön'
    ])
    def test_first_name_valid(self, name):
        self.user.setFirstName(name)
        self.myProfile.enterFirstName(self.user)
        self.myProfile.pressSave()
        mySection = self.myProfile.pressBackArrow()
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
        self.myProfile.pressSave()
        mySection = self.myProfile.pressBackArrow()
        assert mySection.username == old_username
        myProfile = mySection.pressProfileEdit()
        assert myProfile.username == old_username

    def test_username_already_exists(self):
        other_user = User()
        other_user.http.createAccount()
        old_username = self.myProfile.username
        self.user.username = other_user.username
        self.myProfile.enterUsername(self.user)
        self.myProfile.pressSave()
        mySection = self.myProfile.pressBackArrow()
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
