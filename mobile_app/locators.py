from appium.webdriver.common.mobileby import MobileBy
 
 
# convention: 
# affix elements that are buttons with _BUTTON
# affix elements that are input fields with _FIELD
# affix elemens are are check boxes with _CHECKBOX
# affix elements that are lists with _LIST
class BaseSectionLocators:
    THROBBER           = (MobileBy.ID, 'loading_indicator_progressBar')
    PARENT             = (MobileBy.XPATH, "..")
    ITEM_LIST_CONTEXT  = (MobileBy.ID, 'toolbar_main_textview')
    BACK_ARROW_BUTTON  = (MobileBy.XPATH, '//android.widget.ImageButton[@index = "0"]')
    TOAST              = (MobileBy.CLASS_NAME, 'android.widget.Toast')
    
    
class AlertSectionLocators(BaseSectionLocators):
    ALERT_BOX             = (MobileBy.ID, 'parentPanel')
    OK_BUTTON             = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')
    CONFIRM_BUTTON        = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CONFIRM")')
    SUBMIT_BUTTON         = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SUBMIT")')
    CANCEL_BUTTON         = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CANCEL")')
    TITLE                 = (MobileBy.ID, 'alertTitle')
    MESSAGE               = (MobileBy.ID, 'message')
    INPUT_FIELD           = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
    YES_BUTTON            = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("YES")')
    NO_BUTTON             = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NO")')
           
           
class LoginSectionLocators(BaseSectionLocators):
    ACTIVITY = 'com.android.magical.Presentation.Login.LoginActivity'
    
    USERNAME_FIELD         = (MobileBy.ID, 'loginEditText0')
    EMAIL_FIELD            = USERNAME_FIELD
    PASSWORD_FIELD         = (MobileBy.ID, 'loginEditText1')
    FORGOT_PASSWORD_BUTTON = (MobileBy.ID, 'loginForgotPassword')
    LOGIN_BUTTON           = (MobileBy.ID, 'loginSignInButton')
    JOIN_US_BUTTON         = (MobileBy.ID, 'signUpImageButton')

    
class SignupSectionLocators(BaseSectionLocators):
    ACTIVITY = 'com.android.magical.Presentation.SignUp.SignUpActivity'
                              
    USERNAME_FIELD         = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Username")')
    EMAIL_FIELD            = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Email Address")')
    PASSWORD_FIELD         = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Password")')
    RETYPED_PASSWORD_FIELD = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Retype Password")')
    FIRST_NAME_FIELD       = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("First Name")')
    LAST_NAME_FIELD        = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Last Name")')
    SIGNUP_BUTTON          = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SIGN UP")')
    NEXT_BUTTON            = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Next")')                      
    
    
class MainSectionLocators(BaseSectionLocators):
    ACTIVITY = 'com.android.magical.Presentation.MainActivity.MainActivity'
    
    PLUS_BUTTON                 = (MobileBy.ID, 'fab')
    CAMERA_BUTTON               = (MobileBy.XPATH, '//android.widget.LinearLayout[@index = "0"]/android.widget.FrameLayout')
    GALLERY_BUTTON              = (MobileBy.XPATH, '//android.widget.LinearLayout[@index = "1"]/android.widget.FrameLayout')
    ADD_ITEM_BUTTON             = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Item")')
    TOGGLE_FRIENDS_LIST_BUTTON  = (MobileBy.ID, 'main_who_button')
    SETTINGS_BUTTON             = (MobileBy.XPATH, '//android.view.ViewGroup/android.widget.ImageButton')
    ADD_FRIEND_BUTTON           = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Friend")')
    
    
class ItemListSectionLocators(BaseSectionLocators):
    ACTIVITY  = MainSectionLocators.ACTIVITY
    
    ITEM_LIST = (MobileBy.ID, 'main_item_view_container')
    ITEM = (MobileBy.ID, 'main_item_cardview')
    ITEM_NAME_TEXT = (MobileBy.ID, 'main_item_cardview_textview_title')
    BY_TEXT   = (MobileBy.ID, 'main_item_cardview_textview_by')
    NO_ITEMS_FOUND_TEXT = (MobileBy.ID, 'main_item_no_items_text_view') 
    
    
class FriendItemListSectionLocators(ItemListSectionLocators):
    ACTIVITY  = 'com.android.magical.Presentation.ViewFriend.ViewFriendActivity'
    
    ITEM_LIST = (MobileBy.ID, 'view_friend_item_refreshLayout') 
    
    
class HorizontalFriendsListSectionLocators(BaseSectionLocators):
    ACTIVITY = MainSectionLocators.ACTIVITY
    
    FRIENDS_LIST = (MobileBy.ID, 'main_friend_view_container')
    FRIEND       = (MobileBy.ID, 'main_friend_circleimageview')
    FRIEND_NAME  = (MobileBy.ID, 'main_friend_first_name')
    RIGHT_ARROW_BUTTON  = (MobileBy.ID, 'main_friend_view_arrow')
    
class AddItemSectionLocators(BaseSectionLocators):
    ACTIVITY            = 'com.android.magical.Presentation.ItemDetails.ItemDetailsActivity'

    ITEM_NAME_FIELD     = (MobileBy.ID, 'itemDetails_itemName_editText')
    PRICE_FIELD         = (MobileBy.ID, 'itemDetails_price_editText')
    FOR_WHO_BUTTON      = (MobileBy.ID, 'itemDetails_who_layout')
    FOR_WHEN_BUTTON     = (MobileBy.ID, 'itemDetails_when_layout')
    FOR_WHERE_BUTTON    = (MobileBy.ID, 'itemDetails_where_layout')
    WHO_CAN_KNOW_BUTTON = (MobileBy.ID, 'itemDetails_whoCanKnow_layout')
    ADD_ITEM_BUTTON     = (MobileBy.ID, 'itemDetails_saveButton')
    
    
class EditItemSectionLocators(BaseSectionLocators):
    ACTIVITY  = "com.android.magical.Presentation.EditItemDetails.EditItemDetailsActivity"
    
    PRICE_TEXT = (MobileBy.ID, 'edit_item_details_price_edit_text')
    ADD_REVIEW_BUTTON = (MobileBy.ID, 'edit_item_details_add_review_button')
    REVIEW = (MobileBy.ID, 'review_layout_text_layout')
    
    
class ReviewListSectionLocators:
    ACTIVITY  = "com.android.magical.Presentation.EditItemDetails.EditItemDetailsActivity"

    REVIEW = (MobileBy.ID, 'review_layout_text_layout')
    REVIEWER_TEXT = (MobileBy.XPATH, '//android.widget.RelativeLayout[@index="0"]')
    REVIEW_TEXT  = (MobileBy.ID, 'review_layout_text_content')
    
    
class SettingSectionLocators(BaseSectionLocators):
    ACTIVITY = MainSectionLocators.ACTIVITY
    
    LOG_OUT_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Log Out")')
    
    
class ReviewSectionLocators(BaseSectionLocators):
    ACTIVITY = 'com.android.magical.Presentation.AddReview.AddReviewActivity'
    
    REVIEW_TEXT_FIELD = (MobileBy.ID, 'add_review_details_edittext')
    POST_REVIEW_BUTTON = (MobileBy.ID, 'add_review_post_review_button')
    RECOMMEND_CHECKBOX = (MobileBy.ID, 'add_review_recommend_checkbox')
    ONE_STAR_BUTTON = (MobileBy.ID, 'add_review_star1')
    TWO_STAR_BUTTON = (MobileBy.ID, 'add_review_star2')
    THREE_STAR_BUTTON = (MobileBy.ID, 'add_review_star3')
    FOUR_STAR_BUTTON = (MobileBy.ID, 'add_review_star4')
    FIVE_STAR_BUTTON = (MobileBy.ID, 'add_review_star5')
    
    
class AddFriendSectionLocators(BaseSectionLocators):
    ACTIVITY = "com.android.magical.Presentation.AddFriend.AddFriendActivity"

    FIRST_NAME_FIELD = (MobileBy.ID, 'add_friend_first_name_edit_text')
    LAST_NAME_FIELD = (MobileBy.ID, 'add_friend_last_name_edit_text')
    EMAIL_ADDRESS_FIELD = (MobileBy.ID, 'add_friend_email_edit_text')
    SAVE_BUTTON = (MobileBy.ID, 'menu_add_friend_save')
    BACK_ARROW_BUTTON = (MobileBy.XPATH, '//android.widget.ImageButton[@index = "0"]')
    
    
class VerticalFriendsListSectionLocators(BaseSectionLocators):
    ACTIVITY = "com.android.magical.Presentation.FriendList.FriendListActivity"
    
    FRIEND = (MobileBy.ID, 'friendListRelativeLayoutBaseView')
    FRIEND_NAME_TEXT = (MobileBy.ID, 'friendListTextView')
    
    
class FriendEditSectionLocators(BaseSectionLocators):
    ACTIVITY = "com.android.magical.Presentation.EditFriend.EditFriendActivity"
        
    UPLOAD_PHOTO_BUTTON = (MobileBy.ID, 'edit_friend_upload_photo_button')
    FIRST_NAME_FIELD = (MobileBy.ID, 'edit_friend_first_name_edit_text')
    LAST_NAME_FIELD = (MobileBy.ID, 'edit_friend_last_name_edit_text')
    EMAIL_ADDRESS_FIELD = (MobileBy.ID, 'edit_friend_email_edit_text')
    BIRTHDAY_FIELD = (MobileBy.ID, 'edit_friend_birthday_edit_text')
    HAMBURGER_BUTTON = (MobileBy.XPATH, '//android.widget.ImageView[@index = "1"]')
    DELETE_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Delete")')
    SAVE_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAVE")')
    
    
class LoggedinUserSectionLocators(BaseSectionLocators):
    ACTIVITY = "com.android.magical.Presentation.ViewFriend.ViewFriendActivity"
    
   
class FriendSectionLocators(BaseSectionLocators):
    ACTIVITY = "com.android.magical.Presentation.ViewFriend.ViewFriendActivity"
    
    EDIT_FRIEND_BUTTON = (MobileBy.ID, 'menu_view_friend_edit')
    FRIEND_NAME_TEXT = (MobileBy.ID, 'view_friend_toolbar_title_text')