# Selenium

## Background and discussion

For our biopharmaceutical electronic data capture (EDC) system we typically had a large number of custom forms (thirty plus) created for each study deployment to support the data collection needs of the client.  Each form could then have anywhere from thirty to sixty (or more) form elements with various levels of validation applied.

Not only did we need to test these forms for functionality, but we also had to provide validation documentation for each form.  (This was typically done by taking a screenshot of the form being tested in various states and saving it with a time/date stamp.)

Needless to say the QC team was really struggling to test and document everything in a thorough manner within the timelines we were given.  In order to assist them I worked on automating a large percentage of the testing with Selenium, and my efforts also provided the QC team with a working example on which to base further automated test development.  I also needed to support both Linux and Windows systems running the tests.

(Please note that I'm not including the entirety of the coding efforts in this sample; simply a small selection to illustrate the kind of programmatic processes I developed.)

## Sample Files Commentary

### 1 - TestDirector.py

* Entry point for the test suite
* Provides the user with help on the various parameters that can be passed to control how the tests are to be run
* Compiles a list of tests to execute and passes control over to the test runner

### 2 - TestingBaseClass.py

* Implementation of some core functionality to support the greater test suite:
  * Instantiate the web driver (Chrome, Firefox, IE, etc.)
  * Take screenshots of the form being tested at various points including in-image annotations
  * Highlight each form element being tested to provide visual cues and enhance validation screenshots
  * Toggle certain page elements that enabled/disabled other form elements

### 3 - ElementQueryTesting.py

* An actual set of tests run to verify and document the ability to add queries to page elements
