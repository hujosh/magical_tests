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
    #TOAST              = (MobileBy.XPATH, '//[text()="placeholder"]')
    HAMBURGER_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("More options")')
    TOGGLE_CALENDAR_BUTTON = (MobileBy.ID, 'bottom_bar_events')



class LoginSectionLocators(BaseSectionLocators):
    ACTIVITY = 'com.android.magical.Presentation.Login.LoginActivity'

    USERNAME_FIELD = (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="Magical"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField')
    EMAIL_FIELD = USERNAME_FIELD
    PASSWORD_FIELD = (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="Magical"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeSecureTextField')
    FORGOT_PASSWORD_BUTTON = (MobileBy.ACCESSIBILITY_ID, 'Forgot your password?')
    LOGIN_BUTTON = (MobileBy.ACCESSIBILITY_ID, 'LOG IN')
    JOIN_US_BUTTON = (MobileBy.ID, 'JOIN US')


class AlertSectionLocators(BaseSectionLocators):

    ALERT_BOX             = (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeAlert')


    OK_BUTTON             = (MobileBy.ACCESSIBILITY_ID, 'OK')
    #CONFIRM_BUTTON        = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CONFIRM")')
    #SUBMIT_BUTTON         = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SUBMIT")')
    #CANCEL_BUTTON         = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CANCEL")')
    TITLE                 = (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeAlert/XCUIElementTypeStaticText[1]')
    MESSAGE               = (MobileBy.ID, '**/XCUIElementTypeAlert/XCUIElementTypeStaticText[2]')
    INPUT_FIELD           = (MobileBy.XPATH, '//XCUIElementTypeAlert[@name="Forgot password?"]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther')
    #YES_BUTTON            = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("YES")')
    #NO_BUTTON             = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NO")')


class SignupSectionLocators(BaseSectionLocators):
    ACTIVITY = 'com.android.magical.Presentation.SignUp.SignUpActivity'

    USERNAME_FIELD = (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="Magical"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField[1]')
    EMAIL_FIELD = (MobileBy.IOS_PREDICATE, 'wdValue == "Email Address"')
    PASSWORD_FIELD = (MobileBy.IOS_PREDICATE, 'wdValue == "Password"')
    RETYPED_PASSWORD_FIELD = (MobileBy.IOS_PREDICATE, 'wdValue == "Retype Password"')
    FIRST_NAME_FIELD = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("First Name")')
    LAST_NAME_FIELD = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Last Name")')
    SIGNUP_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SIGN UP")')
    NEXT_BUTTON = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Next")')
    TERMS_AND_CONDITIONS_CHECKBOX = (MobileBy.ID, 'createAccountInformationCheckBox')


class ForgotPasswordSectioniOSLocators (AlertSectionLocators):
    INPUT_FIELD  = (MobileBy.XPATH, '//XCUIElementTypeAlert[@name="Forgot password?"]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther')
