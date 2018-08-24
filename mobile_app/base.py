import time
import subprocess

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings

if settings.desired_caps['platformName'] == 'Android':
    from mobile_app.locators import *
else:
    from mobile_app.locators_ios import *

class SectionNotLoaded(Exception):
    pass
    
class ElementNotFound(Exception):
    pass
    
class ItemNotFound(Exception):
    pass
    
class FriendNotFound(Exception):
    pass

class Section(object):
    '''This class contains methods and properties common to all sections.'''
    def __init__(self, driver, timeout = 5):
        self.driver = driver
        self.timeout = timeout
        try:
            self.isSectionLoaded()
        except TimeoutException:
            current_activity = self.driver.current_activity
            raise SectionNotLoaded('"%s" failed to load; waited %s seconds: current activity:%s'%(self.__class__.__name__, self.timeout,current_activity))

    def getSectionName(self):
        return self.__class__.__name__

    def isSectionLoaded(self):
        # We don't consider a section to be loaded if the throbber is still present.
        self.waitForThrobberToDisappear()
        if settings.desired_caps['platformName'] == 'Android':
            activity_loaded = self.driver.wait_activity(self.activity, self.timeout)
            if not(activity_loaded):
                raise TimeoutException
        else:
            time.sleep(5)
            
    def sectionPresent(self):
        try:
            self.isSectionLoaded()
            return True
        except:
            raise AssertionError('"%s" failed to load; waited %s seconds'%(self.__class__.__name__, self.timeout))

    def assertControlPresent(self, control):
        try:
            self.findElement(*control)
            return True
        except ElementNotFound as e:
            raise AssertionError(str(e))


    def findElement(self, *locator, expectedCondition = EC.visibility_of_element_located):
        return self.findElementWait(locator, expectedCondition)
            
    def findElements(self, *locator, expectedCondition = EC.visibility_of_any_elements_located):
        return self.findElementWait(locator, expectedCondition)
        
    def findElementFromElement(self, locator, element, expectedCondition = EC.visibility_of_element_located):
        expected = expectedCondition(locator)
        method = lambda x: lambda y: expected(element)
        return self.findElementWait(locator, method)       
                   
    def findElementWait(self, locator, expectedCondition):
        '''Like findElement, only this waits self.timeout seconds
           for the element specified by locator to be in the state
           specified by expectedConditon.
        '''
        wait = WebDriverWait(self.driver, self.timeout)
        try:
            element = wait.until(expectedCondition(locator))
        except TimeoutException:
            element_name = self._getElementName(locator)
            raise ElementNotFound('Waited %s seconds but couldn\'t find "%s" in "%s.\nStrategy used was "%s""'%(
                    self.timeout, element_name, self.__class__.__name__, str(locator)))
        return element    
        
    def waitForThrobberToDisappear(self):
        time.sleep(1)
        self.findElement(*BaseSectionLocators.THROBBER, 
            expectedCondition = EC.invisibility_of_element_located)

    def enterText(self, element, text, clear = False):
        '''Enter text into the element, and then get rid of the software keyboard.'''
        if clear == True:
            element.clear()
        if text != "":
            element.set_value(text)
            #self.remove_keyboard()

    def flick(self, direction):
        '''flick the screen down, up, left, or right, a little bit.'''
        if direction == 'down':
            directions = (0, 0, 0, 100)
        elif direction == 'up':
            pass
        elif direction == 'left':
            pass
        elif direction == 'right':
            directions = (0, 0, 300, 0)
            pass
        self.driver.swipe(*directions, duration=0)
     
    def remove_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except:
            # This doesn't matter...
            pass


    @property
    def isiOS(self):
        return settings.desired_caps['platformName'] == 'iOS'

    def isAndroid(self):
        return settings.desired_caps['platformName'] == 'Android'

    def _setLoggedinUser(self, user):
        Section.loggedinUser = user
            
    def pressBackArrow(self):
        self.findElement(*self.locator.BACK_ARROW_BUTTON).click()
     
    def _PutAppInBackground(self, background_time =0.5):
        # This is a workaround to a bug
        #time.sleep(1)
        #self.driver.background_app(background_time)
        pass

    def PutAppInBackground(self, background_time=0.5):
        # This is a workaround to a bug
        time.sleep(1)
        self.driver.background_app(background_time)

    def assertToastTextEquals(self, expected_toast_text):
        toast_text = self.toastText
        if toast_text != expected_toast_text:
            raise AssertionError("The toast text should have been '%s' but was '%s'"%(expected_toast_text, toast_text))

    def scroll(self, elements):
        el1 = elements[0]
        el2 = elements[-1]
        x_start = el1.location['x']
        x_end = el2.location['x']
        y_start = el1.location['y']
        y_end = el2.location['y']
        self.driver.swipe(x_start + 300, y_start, x_start, y_start)

    @property
    def toastText(self):
        return self.findElement(*self.locator.TOAST, 
            expectedCondition = EC.visibility_of_element_located).text
    
    def _getElementName(self, locator):
        classes = self.locator.mro()
        for cls in classes:
            for (name, element) in cls.__dict__.items():
                if element == locator:
                    return name
        raise AttributeError("The locator %s does not exist in locators.py"%(str(locator)))

    def pressHamburger(self):
        self.findElement(*self.locator.HAMBURGER_BUTTON).click()


class PhoneNetwork:
    def __init__(self):
        pass

    def _set_wifi(self, status):
        subprocess.run("adb shell am broadcast -a io.appium.settings.wifi --es setstatus %s" % status, shell=True)

    def _set_data(selfself, status):
        subprocess.run("adb shell svc data %s" % status, shell=True)

    def set_network_connection(self, status):
        self._set_wifi(status)
        self._set_data(status)

