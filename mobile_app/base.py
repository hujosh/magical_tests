import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mobile_app.locators import *


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
            raise SectionNotLoaded('"%s" failed to load; waited %s seconds'%(self.__class__.__name__, self.timeout))
           
    def isSectionLoaded(self):
        # We don't consider a section to be loaded if the throbber is still present.
        self.waitForThrobberToDisappear()
        activity_loaded = self.driver.wait_activity(self.activity, self.timeout)
        if not(activity_loaded):
            raise TimeoutException
            
    def sectionPresent(self):
        try:
            self.isSectionLoaded()
            return True
        except:
            return False
         
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
        
    def enterText(self, element, text):
        '''Enter text into the element, and then get rid of the software keyboard.'''
        element.clear()
        if text != "":
            element.set_value(text)
            self.remove_keyboard()
           
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
        self.driver.swipe(*directions, duration=800)
     
    def remove_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except:
            # This doesn't matter...
            pass
     
    def _setLoggedinUser(self, user):
        Section.loggedinUser = user
            
    def pressBackArrow(self):
        self.findElement(*self.locator.BACK_ARROW_BUTTON).click()
     
    def _PutAppInBackground(self):
        # This is a workaround to a bug
        time.sleep(1)
        self.driver.background_app(0.5)
        pass
        
    def assertToastTextEquals(self, expected_toast_text):
        toast_text = self.toastText
        if toast_text != expected_toast_text:
            raise AssertionError("The toast text should have been '%s' but was '%s'"%(expected_toast_text, toast_text))

    @property        
    def toastText(self):
        return self.findElement(*self.locator.TOAST, 
            expectedCondition = EC.presence_of_element_located).text
    
    def _getElementName(self, locator):
        classes = self.locator.mro()
        for cls in classes:
            for (name, element) in cls.__dict__.items():
                if element == locator:
                    return name
        raise AttributeError("The locator %s does not exist in locators.py"%(str(locator)))