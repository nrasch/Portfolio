import unittest

import time
from time import strftime

import sys

from ElementTwiddle import ElementTwiddle
from edcFormElement import EDCFormElement

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

class TestingBaseClass(unittest.TestCase):
  sleepTime = 4
  os = "linux"
  afterLoginURL = ""
  
  #----------------------------------------------------------------------------#
  def __init__(self, testName, studyObject, driver, user, form, element):
    super(TestingBaseClass, self).__init__(testName)
    self.studyObject = studyObject
    self.study = self.studyObject.study
    self.baseURL = studyObject.baseURL
    self.driver = driver
    self.user = user["user"]
    self.passw = user["pass"]
    self.role = user["role"]
    self.element = element
    self.form = form
    self.formAddURL = self.baseURL + studyObject.forms[self.form]["addURL"]
    self.formViewURL = self.baseURL + studyObject.forms[self.form]["viewURL"]
    
    if element != "":
      self.screenshotLabel = self.driver + "-" + self.study + "-" + self.role + \
        "-" + self.form + "-" + self.element.id
    else:
      self.screenshotLabel = self.driver + "-" + self.study + "-" + self.role + \
        "-" + self.form
        
    if sys.platform == "win32":
      self.os = "windows"

  #----------------------------------------------------------------------------#
  def setUp(self):
    # If you put the buildDriver call into the __init__ method the user will end
    # up with a seperate browser open for each test added to the suite!  Not
    # good, so we keep it down here.  This will instantiate a new browser only
    # when the test is run, one at a time.
    self.buildDriver(self.driver)
    self.twiddler = ElementTwiddle(self)
    self.login()

  #----------------------------------------------------------------------------#
  def login(self):
    self._driver.get(self.baseURL + "/login");
    
    time.sleep(self.sleepTime)
    
    userField = self._driver.find_element_by_name("data[User][email]")
    passField = self._driver.find_element_by_name("data[User][password]")
    
    userField.send_keys(self.user)
    passField.send_keys(self.passw)

    self._driver.find_element_by_class_name('btn').click()
    time.sleep(self.sleepTime)
    
    self._driver.get(self.afterLoginURL)
    time.sleep(self.sleepTime)
    
  #----------------------------------------------------------------------------#
  def buildDriver(self, driver):
    if driver == "Chrome":
      chrome_options = Options()
      
      if self.os == "windows":
        self._driver = webdriver.Chrome(chrome_options=chrome_options)
      else:
        self._driver = webdriver.Remote(
          command_executor='http://127.0.0.1:4444/wd/hub',
          desired_capabilities=DesiredCapabilities.CHROME)      
      
    elif driver == "Firefox":
      self._driver = webdriver.Firefox()
    
    elif driver == "IE":
      caps = DesiredCapabilities.INTERNETEXPLORER
      caps['ignoreProtectedModeSettings'] = True
      
      if self.os == "windows":
        self._driver = webdriver.Ie(capabilities=caps)
      else:
        self._driver = webdriver.Remote(
          command_executor='http://127.0.0.1:4444/wd/hub',
          desired_capabilities=caps)

    else:
      raise SyntaxError("Unsupported driver type argument passed to method")
    
    self._driverType = driver
  
  #----------------------------------------------------------------------------#
  def logScreen(self, title):
      if self.os == "windows":
        imgName = ".\\test_results\\" + title + '.png'
      else:
        imgName = "/home/ubuntu/selenium/test_results/" + title + '.png'
      
      imgLabel = title
      self._driver.save_screenshot(imgName)

      img = Image.open(imgName)
      width, height = img.size
      xcoor = 10
      ycoor = height - 70

      draw = ImageDraw.Draw(img)
      
      if self.os == "windows":
        font = ImageFont.truetype("calibri.ttf", 28)
      else:
        font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf", 22)
      
      draw.text((xcoor, ycoor), imgLabel, font=font, fill=(255,0,0,255) )

      ycoor = ycoor + 25
      draw.text((xcoor, ycoor), strftime("%Y-%b-%d %H:%M:%S"), font=font, fill=(255,0,0,255) )

      img.save(imgName)

  #----------------------------------------------------------------------------#
  def highlight(self, element, level="parent"):
      """Highlights a Selenium Webdriver element"""
      
      elements = []
      
      if isinstance(element, EDCFormElement):
        if element.type == 'udate':
          for name in element.eValueNames:
            elements.append(self._driver.find_element_by_name(name))
        else:
          elements.append(self._driver.find_element_by_name(element.eName))
      
      else:
        elements.append(element)
      
      for e in elements:
        if level == "element":
          item = e
        elif level == "parent":
          item = e.find_element_by_xpath('..')
        elif level == "grandparent":
          item = e.find_element_by_xpath('..').find_element_by_xpath('..')

        def apply_style(s):
          try:
            self._driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", item, s)
            return True
          except:
              return False

        apply_style("background: yellow; border: 2px solid red;")
#----------------------------------------------------------------------------#
  def toggle(self, toggleElements):
    """Clicks the page element that enables/disables other element(s) on the page"""
    for toggle in toggleElements:
      self.twiddler.twiddle(toggle["id"], toggle["eName"], \
        toggle["eValueId"], toggle["type"], "click")