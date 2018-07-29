from TestingBaseClass import TestingBaseClass
from ElementFormTesting import ElementFormTesting
from ElementQueryTesting import ElementQueryTesting
from AccessAddFormTesting import AccessAddFormTesting
from AccessCannotAddFormTesting import AccessCannotAddFormTesting

import unittest
from StudyDataLoader import StudyDataLoader
from concurrencytest import ConcurrentTestSuite, fork_for_tests
import argparse
import sys

def getTests(suiteObj):
  tests = []
  for method in dir(suiteObj):
    if "test_" in method:
      tests.append(method)
  return tests


if __name__ == "__main__":
  
  suite = unittest.TestSuite()
  loader = StudyDataLoader()
  
  drivers = ["Chrome", "IE"]
  protocols = ["SA001-202-SLIM"]
  
  testSuites = {
    "ElementFormTesting":{
      "users":"usersAddFormsYes"
    },
    "ElementQueryTesting":{
      "users":"usersAddQueriesYes"
    },
    "AccessAddFormTesting":{
      "users":"usersAddFormsYes"
    },
    "AccessCannotAddFormTesting":{
      "users":"usersAddFormsNo"
    },
  }
  
  parser = argparse.ArgumentParser(description='Execute one or more Selenium test suites.')

  parser.add_argument('-s', '--suites', action = 'store',
    dest = 'suites', metavar = '',
    help='comma delimited list of suites to execute; NO SPACES')
    
  parser.add_argument('-d', '--drivers', action = 'store',
    dest = 'drivers', metavar = '',
    help='comma delimited list of drivers to test against; NO SPACES')
    
  parser.add_argument('-p', '--protocols', action = 'store',
    dest = 'protocols', metavar = '',
    help='comma delimited list of protocols to test against; NO SPACES')
    
  parser.add_argument('-l', '--list', action='store_true',
  help='return a list of avaiable test parameter values')
  
  parser.add_argument('--forms-for', action = 'store',
    dest = 'formsFor', metavar = '',
    help='the protocol for which to list associated forms')
    
  parser.add_argument('--tests-for', action = 'store',
    dest = 'testsFor', metavar = '',
    help='the suite for which to list associated tests')
    
  parser.add_argument('-t', '--tests', action = 'store',
    dest = 'argTests', metavar = '', default="All",
    help='comma delimited list of tests to execute; NO SPACES')
    
  parser.add_argument('-f', '--forms', action = 'store',
    dest = 'argForms', metavar = '', default="All",
    help='comma delimited list of forms to test against; NO SPACES')
    
  args = parser.parse_args()

  if args.list:
    print("")
    print("Test suites avaiable:")
    print(", ".join(testSuites.keys()) + ", All")
    print("")
    print("Drivers avaiable:")
    print(", ".join(drivers) + ", All")
    print("")
    print("Protocols avaiable:")
    print(", ".join(protocols))
    print("")
    print("Ex:  python TestDirector.py -s ElementFormTesting -d Chrome -p SA001-202-SLIM")
    print("Ex:  python TestDirector.py -s ElementFormTesting,ElementQueryTesting -d Chrome,IE -p SA001-202-SLIM")
    sys.exit(0)
  
  if args.formsFor:
    try:
      studyObj = loader.loadStudyDataFile(args.formsFor)
      studyForms = studyObj.forms.keys()
      
      print("")
      print("Forms avaiable for " + args.formsFor +":")
      print("")
      for form in studyForms:
        print(form)
      print("All")
      print("")
    except:
      print("")
      print("Error:  Protocol " + args.formsFor + " not found.  Try the '--list' option for supported protocols.")
      print("")
    finally:
      exit()

  if args.testsFor:
    try:
      suiteObj = globals()[args.testsFor]
      tests = getTests(suiteObj)
      
      print("")
      print("Tests avaiable for " + args.testsFor +":")
      print("")
      for test in tests:
        print(test)
      print("All")
      print("")
    except:
      print("")
      print("Error:  Test suite " + args.testsFor + " not found.  Try the '--list' option for supported test suites.")
      print("")
    finally:
      exit()    

  if args.suites:
    suitesToRun = args.suites.split(",")
  
  if args.drivers:
    driversToRun = args.drivers.split(",")
    
  if args.protocols:
    protocolsToRun = args.protocols.split(",")
    
  formsToRun = args.argForms.split(",")
  testsToRun = args.argTests.split(",")
  
  try:
    suitesToRun, driversToRun, protocolsToRun
  except NameError:
    print("")
    print("Error:  Test suite, driver, and protocol must be given")
    print("")
    print("Ex:  python TestDirector.py -s ElementFormTesting -d Chrome -p SA001-202-SLIM")
    print("Ex:  python TestDirector.py -s ElementFormTesting,ElementQueryTesting -d Chrome,IE -p SA001-202-SLIM")
    sys.exit(2)
  
  # ensure parameters given are actually valid
  if "All" in suitesToRun:
    suitesToRun = testSuites
  if "All" in driversToRun:
    driversToRun = drivers
    
  suitesToRun = list(set(suitesToRun) & set(testSuites.keys()))
  driversToRun = list(set(driversToRun) & set(drivers))
  protocolsToRun = list(set(protocolsToRun) & set(protocols))

  if (len(suitesToRun)) == 0 or (len(driversToRun)) == 0 or (len(protocolsToRun)) == 0:
    print("")
    print("Error:  Valid test suite, driver, and protocol values must be given")
    print("")
    print("Ex:  python TestDirector.py -s ElementFormTesting -d Chrome -p SA001-202-SLIM")
    print("Ex:  python TestDirector.py -s ElementFormTesting,ElementQueryTesting -d Chrome,IE -p SA001-202-SLIM")
    print("")
    print("Try running 'python TestDirector.py --list' without the qoutes for more information")
    sys.exit(2)

    
  for suiteItem in suitesToRun:
    for driver in driversToRun:
      for protocol in protocolsToRun:
        
        studyObj = loader.loadStudyDataFile(protocol)
        suiteObj = globals()[suiteItem]
        studyForms = studyObj.forms.keys()
        tests = getTests(suiteObj)
        
        if "All" in formsToRun:
          formsToRun = studyForms
        formsToRun = list(set(formsToRun) & set(studyForms))
        
        if "All" in testsToRun:
          testsToRun = tests
        testsToRun = list(set(testsToRun) & set(tests))
        
        for user in getattr(studyObj, testSuites[suiteItem]["users"]):
          for form in formsToRun:
            for test in testsToRun:
              
              if "Element" in suiteItem:
                elist = loader.loadStudyDataJson(protocol, form)
                for element in elist:
                  suite.addTest(suiteObj(
                    test, studyObj, driver, user, form, element
                  ))

              if "Access" in suiteItem:
                suite.addTest(suiteObj(
                  test, studyObj, driver, user, form, ""
                ))
      
      
  if sys.platform == "win32":
    unittest.TextTestRunner(verbosity=0).run(suite)
  else:
    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(2))
    unittest.TextTestRunner(verbosity=0).run(concurrent_suite)
