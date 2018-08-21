import os


global host
host =  'http://localhost:4723/wd/hub'
# Information about the phone; all tests use this dictionary...
global desired_caps
desired_caps = {}



#desired_caps['deviceName'] = 'D1AGAS3770501528'
#desired_caps['deviceName'] = 'emulator-5554'
desired_caps['deviceName'] = 'SM-G9201'
# Returns abs path relative to this file and not cwd
desired_caps['app'] = os.path.abspath(r'apps/magical-dev-debug.apk')
desired_caps['appPackage'] = 'magicalconnect.android.magical.dev'
desired_caps['appActivity'] = 'com.android.magical.Presentation.SplashScreen.SplashScreenActivity'
desired_caps['browserName'] = ""
desired_caps['appiumVersion'] = "1.8.1"
desired_caps['deviceOrientation'] = "portrait"
desired_caps['platformName'] = "Android"
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"]= True
desired_caps["automationName "]= 'UIAutomator2'
#desired_caps["platformVersion"] = "7.1"
desired_caps["platformVersion"] = "7.0"


'''
desired_caps["automationName"]= "XCUITest"
desired_caps["platformName"]= "iOS"
desired_caps["platformVersion"]= "11.4"
desired_caps["deviceName"] ="iPhone X"
desired_caps["app"]= "/Users/magadmin/Library/Developer/Xcode/DerivedData/Magical-cwqsdygvybitlyeymrrewwdhlgph/Build/Products/Debug-iphonesimulator/Magical.app"
desired_caps["autoAcceptAlerts"]=True
'''


