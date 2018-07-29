from TestingBaseClass import TestingBaseClass
import unittest
import time
from StudyDataLoader import StudyDataLoader
from subprocess import call
from concurrencytest import ConcurrentTestSuite, fork_for_tests

class ElementQueryTesting(TestingBaseClass):
  
  #----------------------------------------------------------------------------#
  def __init__(self, testName, baseURL, driver, user, form, element):
    super(ElementQueryTesting, self).__init__(testName, baseURL, driver, user, form, element)
    self.afterLoginURL = self.formViewURL

  #----------------------------------------------------------------------------#
  def setUp(self):
    if self.os == "windows":
      # todo: remove hard coding to my implementation of cygwin on windows
	  cmd = "E:\\WinApps\\cygwin\\bin\\bash.exe /cygdrive/c/Users/Nathan/Documents/GitHub/selenium/bashscripts/SA001202-Create-Forms.sh"
    else:
      cmd = "/bin/bash -c /home/ubuntu/selenium/bashscripts/SA001202-Create-Forms.sh"
    call(cmd, shell=True)

    super(ElementQueryTesting, self).setUp()
  
  #----------------------------------------------------------------------------#
  def tearDown(self):
    self._driver.quit()
    if self.os == "windows":
	  # todo: remove hard coding to my implementation of cygwin on windows
      cmd = "E:\\WinApps\\cygwin\\bin\\bash.exe /cygdrive/c/Users/Nathan/Documents/GitHub/selenium/bashscripts/cleanQueriesSA001202.sh"
    else:
      cmd = "/bin/bash -c /home/ubuntu/selenium/bashscripts/cleanQueriesSA001202.sh"
    call(cmd, shell=True)
  
  #----------------------------------------------------------------------------#
  def clickQueryManagerTab(self, tabName):
    tabs = self._driver.find_elements_by_css_selector("a.ui-tabs-anchor")
    for tab in tabs:
      if tab.get_attribute("innerHTML") == tabName:
        tab.click()
        self.highlight(tab)
        time.sleep(1)
        break
  
  #----------------------------------------------------------------------------#
  def populateQueryItem(self, qText, qLabel = ""):
    queryText = self._driver.find_element_by_id("data[Query][query]")
    queryText.send_keys(self.element.id + " " + qText)
    
    self.highlight(queryText, "element")
    self.highlight(self._driver.find_element_by_css_selector("span#QueryElementText"), "element")
    
    if qLabel != "":
      self.logScreen(self.screenshotLabel + qLabel)
    self._driver.find_element_by_id("btnsubmit").click()
    time.sleep(self.sleepTime)
  
  #----------------------------------------------------------------------------#
  def selectQueryType(self, type):
    queryType = self._driver.find_element_by_id("data[Query][query_type_id]")
    for option in queryType.find_elements_by_tag_name('option'):
      if option.text == type:
        option.click()
    self.highlight(queryType, "element")

  #----------------------------------------------------------------------------#
  def deleteQueries(self, deleteButtons):
    for button in deleteButtons:
      button.click()
      time.sleep(1)
      alert = self._driver.switch_to_alert()
      alert.accept()
      time.sleep(self.sleepTime)
      alert = self._driver.switch_to_alert()
      alert.accept()
      time.sleep(self.sleepTime)
      
  #----------------------------------------------------------------------------#
  def checkQueryTableContents(self, tableID, test, label = ""):
    queryOpen = self._driver.find_element_by_id(tableID)
    queryOpenTable = queryOpen.find_element_by_id("openQuery")
    if test:
      self.assertTrue("No records found" in queryOpenTable.get_attribute("innerHTML"))
    else:
      self.assertFalse("No records found" in queryOpenTable.get_attribute("innerHTML"))
    self.highlight(queryOpenTable, "element")
    
    if label != "":
      self.logScreen(self.screenshotLabel + label)
    
    return queryOpen
  
  #----------------------------------------------------------------------------#
  def closeQueryManager(self, label = ""):
    # close query manager
    self._driver.find_element_by_css_selector("span.ui-button-icon-primary.ui-icon.ui-icon-closethick").click()
    time.sleep(1)
    
    # screenshot now highlighted page element
    if label != "":
      self.logScreen(self.screenshotLabel + label)
    
  #----------------------------------------------------------------------------#
  def test_elementIsQueryable(self):
    print(self.screenshotLabel + " Assert element is queryable")

    # click element to instantiate query popup
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # verify query popup appears and screenshot
    result = False
    for element in self._driver.find_elements_by_class_name("ui-dialog-title"):
      if element.get_attribute("innerHTML") == "Query Manager":
        result = True
    
    self.assertTrue(result)
    
    self.highlight(self._driver.find_element_by_css_selector("span#QueryElementText"), "element")
    self.logScreen(self.screenshotLabel + "-Queryable")
  
  #----------------------------------------------------------------------------#
  def test_elementCreateQuery(self):
    print(self.screenshotLabel + " Assert query can be created for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Query")
    
    # populate query
    self.populateQueryItem("automated query test", "-Query-Create-Values")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Open Queries")
    
    # ensure the new query was created and shows up in the query manager
    self.checkQueryTableContents("Open-Query", False, "-Query-Created-Manager")
    
    # close query manager
    self.closeQueryManager("-Query-Created-Page")
    
  #----------------------------------------------------------------------------#
  def test_elementCreateProtocolDeviation(self):
    print(self.screenshotLabel + " Assert protocol deviation can be created for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Protocol deviation")
    
    # populate query
    self.populateQueryItem("automated protocol deviation test", "-PD-Create-Values")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Protocol Deviations")
    
    # ensure the new query was created and shows up in the query manager
    self.checkQueryTableContents("Protocol-Deviations", False, "-PD-Created-Page")
    
    # close query manager
    self.closeQueryManager("-PD-Created-Page")
  
  #----------------------------------------------------------------------------#
  def test_elementCreateGeneralComment(self):
    print(self.screenshotLabel + " Assert general comment can be created for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("General comment")
    
    # populate query
    self.populateQueryItem("automated general comment test", "-GC-Create-Values")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("General Comments")
    
    # ensure the new query was created and shows up in the query manager
    self.checkQueryTableContents("General-Comments", False, "-GC-Created-Manager")
    
    # close query manager
    self.closeQueryManager("-GC-Created-Page")
   
  #----------------------------------------------------------------------------#
  def test_deleteQuery(self):
    print(self.screenshotLabel + " Assert query can be deleted for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Query")
    
    # populate query
    self.populateQueryItem("automated query test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Open Queries")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("Open-Query", False, "-Query-To-Delete-Manager")
    
    # delete all queries on element
    self.deleteQueries(queryOpen.find_elements_by_css_selector("a.confirm_delete.btn.btn-info"))
    self.checkQueryTableContents("Open-Query", True, "-Query-Deleted-Manager")
    
    # close query manager
    self.closeQueryManager("-Query-Deleted-Page")
    
  #----------------------------------------------------------------------------#
  def test_deleteProtocolDeviation(self):
    print(self.screenshotLabel + " Assert protocol deviation can be deleted for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Protocol deviation")
    
    # populate query
    self.populateQueryItem("automated protocol deviation test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Protocol Deviations")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("Protocol-Deviations", False, "-PD-To-Delete-Manager")
    
    # delete all queries on element
    self.deleteQueries(queryOpen.find_elements_by_css_selector("a.confirm_delete.btn.btn-info"))
    self.checkQueryTableContents("Protocol-Deviations", True, "-PD-Deleted-Manager")
    
    # close query manager
    self.closeQueryManager("-PD-Deleted-Page")
    
  #----------------------------------------------------------------------------#  
  def test_deleteGeneralComment(self):
    print(self.screenshotLabel + " Assert general comment can be deleted for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("General comment")
    
    # populate query
    self.populateQueryItem("automated general comment test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("General Comments")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("General-Comments", False, "-GC-To-Delete-Manager")
    
    # delete all queries on element
    self.deleteQueries(queryOpen.find_elements_by_css_selector("a.confirm_delete.btn.btn-info"))
    self.checkQueryTableContents("General-Comments", True, "-GC-Deleted-Manager")
    
    # close query manager
    self.closeQueryManager("-GC-Deleted-Page")

  #----------------------------------------------------------------------------#  
  def test_addQueryPost(self):
    print(self.screenshotLabel + " Assert query post can be created for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Query")
    
    # populate query
    self.populateQueryItem("automated query test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Open Queries")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("Open-Query", False, "-Query-To-Post")
    
    queryOpen.find_element_by_css_selector("a.btn.btn-info.AddPost").click()
      
    time.sleep(1)
    post = self._driver.find_element_by_id("QueryPostPost")
    post.send_keys(self.element.id + " automated query post test")

    self.highlight(self._driver.find_element_by_id("QueryPostAddPostForm"), "element")
    self.logScreen(self.screenshotLabel + "Query-Post-Create-Values")
    
    self._driver.find_element_by_id("postSubmit").click()
    time.sleep(self.sleepTime)
    
    result = False
    cells = self._driver.find_elements_by_css_selector("td")
    
    for cell in cells:
      if cell.get_attribute("innerHTML") == self.element.id + " automated query post test":
        result = True
        self.highlight(cell, "grandparent")
        self.logScreen(self.screenshotLabel + "-Query-Post")
        break
        
    self.assertTrue(result)
    self._driver.find_element_by_id("btnReturnToQueries").click()
    time.sleep(1)
      
    # close query manager
    self.checkQueryTableContents("Open-Query", False, "-Query-Posted-To")
    self.closeQueryManager()

  #----------------------------------------------------------------------------#  
  def test_addProtocolDeviationPost(self):
    print(self.screenshotLabel + " Assert protocol deviation post cannot be created for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Protocol deviation")
    
    # populate query
    self.populateQueryItem("automated protocol deviation test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Protocol Deviations")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("Protocol-Deviations", False, "-PD-To-Post")
    
    # assert that a post cannot be added to the PD
    queryOpen.find_element_by_css_selector("a.btn.btn-info.AddPost").click()
    time.sleep(1)
    
    result = False
    cells = self._driver.find_elements_by_css_selector("td")
    
    for cell in cells:
      if cell.get_attribute("innerHTML") == "Adding posts to a Protocol Deviation is not allowed.":
        result = True
        self.highlight(cell, "grandparent")
        self.logScreen(self.screenshotLabel + "PD-No-Add-Post")
        break
    
    self.assertTrue(result)
    self._driver.find_element_by_id("btnReturnToQueries").click()
      
    # close query manager
    self.closeQueryManager()
    
  #----------------------------------------------------------------------------#  
  def test_addGeneralCommentPost(self):
    print(self.screenshotLabel + " Assert general comment post can be created for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("General comment")
    
    # populate query
    self.populateQueryItem("automated general comment test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("General Comments")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("General-Comments", False, "-GC-To-Post")
    
    queryOpen.find_element_by_css_selector("a.btn.btn-info.AddPost").click()
      
    time.sleep(1)
    post = self._driver.find_element_by_id("QueryPostPost")
    post.send_keys(self.element.id + " automated general comment post test")

    self.highlight(self._driver.find_element_by_id("QueryPostAddPostForm"), "element")
    self.logScreen(self.screenshotLabel + "GC-Post-Create-Values")
    
    self._driver.find_element_by_id("postSubmit").click()
    time.sleep(self.sleepTime)
    
    result = False
    cells = self._driver.find_elements_by_css_selector("td")
    
    for cell in cells:
      if cell.get_attribute("innerHTML") == self.element.id + " automated general comment post test":
        result = True
        self.highlight(cell, "grandparent")
        self.logScreen(self.screenshotLabel + "-GC-Post")
        break
    
    self.assertTrue(result)
    self._driver.find_element_by_id("btnReturnToQueries").click()
    time.sleep(1)
    
    # close query manager
    self.checkQueryTableContents("General-Comments", False, "-GC-Posted-To")
    self.closeQueryManager()
    
  #----------------------------------------------------------------------------#
  def test_closeQuery(self):
    print(self.screenshotLabel + " Assert query can be closed for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("Query")
    
    # populate query
    self.populateQueryItem("automated query test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("Open Queries")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("Open-Query", False, "-Query-To-Close")
    queryOpen.find_element_by_css_selector("a.btn.btn-info.AddPost").click()
    time.sleep(self.sleepTime)
    
    # close query
    closeButton = self._driver.find_element_by_id("closeQuerySubmit")
    self.highlight(closeButton, "element")
    time.sleep(1)
    self.logScreen(self.screenshotLabel + "-Query-Closing")
    closeButton.click()
    
    time.sleep(1)
    alert = self._driver.switch_to_alert()
    alert.accept()
    time.sleep(self.sleepTime)
    
    self.checkQueryTableContents("Open-Query", True, "-Query-Closed-Manager")
    
    # close query manager
    self.closeQueryManager("-Query-Closed-Page")
    
  #----------------------------------------------------------------------------#
  def test_closeGeneralComment(self):
    print(self.screenshotLabel + " Assert general comment can be closed for element")
    
    # click element to instantiate query manager
    self._driver.find_element_by_css_selector("div.form_query_element." + self.element.id).click()
    time.sleep(1)
    
    # select query type
    self.selectQueryType("General comment")
    
    # populate query
    self.populateQueryItem("automated general comment test")
    
    # confirm query appears in query manager
    self.clickQueryManagerTab("General Comments")
    
    # ensure the new query was created and shows up in the query manager
    queryOpen = self.checkQueryTableContents("General-Comments", False, "-GC-To-Close")
    queryOpen.find_element_by_css_selector("a.btn.btn-info.AddPost").click()
    time.sleep(self.sleepTime)
    
    # close query
    closeButton = self._driver.find_element_by_id("closeQuerySubmit")
    self.highlight(closeButton, "element")
    time.sleep(1)
    self.logScreen(self.screenshotLabel + "-GC-Closing")
    closeButton.click()
    
    time.sleep(1)
    alert = self._driver.switch_to_alert()
    alert.accept()
    time.sleep(self.sleepTime)
    
    self.checkQueryTableContents("General-Comments", True, "-GC-Closed-Manager")
    
    # close query manager
    self.closeQueryManager("-GC-Closed-Page")