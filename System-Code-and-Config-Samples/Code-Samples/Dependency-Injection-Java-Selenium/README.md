# Dependency Injection with Java and Selenium

The sample code in this folder illustrates the use of dependency injection via a set of automated tests utilizing Selenium and Java.  There are two opportunities for dependency injection in this example:  test results logging and webdriver creation.

## Test Results Logging
Our sample project needs to support three test result logging options: Java’s Reporter implementation, to a database, or into a flat file.

Irrespective of which logging method we utilize we want to decouple the class that utilizes the logging functionality from the details of the logging class’ implementation.  This allows us to swap out the logging class (or perhaps introduce a completely new type of logging class in the future) the reporting suite utilizes without having to touch the implementing class.  With this design we can now be flexible, easily test our code with mocks for example, and support another SOLID design principle:  Classes should be open for extension but closed for modification.

### Implementation
So, how did we do this?

1) Create an interface for the logging functionality (**ILlogger.java**)
```java
public interface ILogger {
  // Define our method signature that each concrete class implementing
  // the interface will populate
  public void log(String message);
}
```

2) Implement the interface with a concrete logging class (**ReportLogger.java**)
```java
// Our concrete class that implements the ILogger interface...
public class ReportLogger implements ILogger{
	
	private StackTraceElement[] stackTraceElements;
	private String className;

	@Override
	public void log(String message) {
		this.stackTraceElements = Thread.currentThread().getStackTrace();
		this.className = stackTraceElements[2].getClassName();
		
		Reporter.log(this.className + " :: " + message);	
	}

}
```

3) “Inject” the logger object into the utilizing class (**ZipcodeSearchFactory.java**)
  * First we create the proper class implementing the ILogger interface
```java
	private void createLogger(String logger) {
		if (logger == "DBLogger") {
			this.logger = new DBLogger();
		} else if (logger == "FlatFileLogger") {
			this.logger = new FlatFileLogger();
		} else {
			// ReportLogger is default
			this.logger = new ReportLogger();
		}
	}
```

  * Next we “inject” the logging class instantiation into the class which will be utilizing the logging object
```java
		// Pull five random zip codes for testing
		ArrayList<HashMap<String, String>> zipsToTest = ZipCodes.getRandomZipcodes(5);
			
		Object[] result = new Object[zipsToTest.size()];
		
		// OK, create each test suite item and “inject” the instantiated logging object into it
		// via its constructor
		for (int i = 0; i < zipsToTest.size(); i++) {
			result[i] = new ZipcodeSearch(this.logger, this.settings, zipsToTest.get(i));
        }
		return result;
```

5) Now the utilizing class exercises the methods of the logging object (**ZipcodeSearch.java**)
  * Let’s use the instantiated logging object without having to worry about the concrete implementation details…
```java
public class ZipcodeSearch extends ABaseTestingClass{
	// Our constructor which takes a class implementing the ILogger interface
	public ZipcodeSearch(ILogger logger, Settings settings, HashMap<String, String> zipcode) {
		this.logger = logger;
		…
```

```java
	@Test
	public void searchByZipcode() throws InterruptedException {
		…
		// And now we utilize the logging object without having to know or worry
		// about how its implementation details occur withing in the class itself
		this.logger.log("Searching for zipcode " + this.zipcode.get("zip"));
		…
```

6) And we can now examine a sample of the test results logging output:
```
Messages
searchTesting.ZipcodeSearch :: Validating zipcode search data for 80909
searchTesting.ZipcodeSearch :: Checking list-view-item content data for zero values and/or missing images
searchTesting.ZipcodeSearch :: Failure. Page contained 2 entries with 0 bathrooms.
```

## WebDriver Creation

The sample code in this folder also has an example of achieving the benefits of dependency injection in a theoretical case where we might not be able to pass a lower level class to a higher level one via the constructor.  We still want the benefits of dependency injection (flexibility, open for extension but closed for modification, passing in mocks for testing, etc.) even though we can't implement it in a text book fashion (i.e. via the constructor).

So, how did we do this?

1) Create an interface for the WebDriver functionality (**IDriverManager.java**)
```java
public interface IDriverManager {
	public WebDriver getDriver(Settings settings) throws MalformedURLException;
}
```

2) Implement the interface with a concrete WebDriver class (**LocalDriverManager.java**)
```java
// Our concrete class that implements the IDriverManager interface...
public class LocalDriverManager implements IDriverManager {
	
	…
	
	/**
	 * Instantiate and configure requested webdriver instance and return to caller
	 */
	public WebDriver getDriver(Settings settings) {
		this.logger.log("Requested driver: " + settings.getBrowser());
		this.logger.log("Requested implicitlyWait: " + settings.getImplicitlyWait().toString());
		
		WebDriver driver;
		
		if (settings.getBrowser().equalsIgnoreCase("ie")) {
			System.setProperty("webdriver.ie.driver", "/home/nathanrasch/ie-driver/IEDriverServer.exe");
			driver = new InternetExplorerDriver();
		} else if (settings.getBrowser().equalsIgnoreCase("chrome")) {
			driver = new ChromeDriver();
		} else {
			driver = new FirefoxDriver();
		}
		
		// set global, Implicit Wait for the driver - http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#implicit-waits
		driver.manage().timeouts().implicitlyWait(settings.getImplicitlyWait(), TimeUnit.SECONDS);
		driver.manage().window().maximize();
		
		this.logger.log("Driver created.  Returning driver object to calling entity.");
		
		return driver;
	}
}
```

3) Utilize the WebDriver object in a way that emulates dependency injection (**ABaseTestingClass.java**)
  * First we make a call to the method that create the proper WebDriver before the test executes
```java
	/**
	 * Before each test create the proper WebDriver and browse to the base testing URL 
	 */
	@BeforeMethod
	public void beforeMethod() throws InterruptedException, MalformedURLException {
		this.createDriverManager(this.settings.getDriverManager());
		this.driver.get(this.settings.getBaseURL());
	}
```

	* Next use a factory pattern to instantiate the concrete WebDriver object and assign it to an internal property
```java
/**
	 * Instantiates concrete implementation of the IDriverManager interface.
	 * 
	 * (LocalDriverManager is default.)
	 */
	protected void createDriverManager(String driverManager) throws MalformedURLException {
		if (driverManager == "RemoteDriverManager") {
			this.driverManager = new RemoteDriverManager(this.logger);
		} else {
			this.driverManager = new LocalDriverManager(this.logger);
		}
		this.driver = this.driverManager.getDriver(this.settings);
	}
```

4) And finally let's use the instantiated WebDriver without having to worry about the internal details of how its implemented or operates (**ZipcodeSearch.java**)
```java
		// search for zipcode
		this.driver.findElement(By.id("input-location")).sendKeys(this.zipcode.get("zip"));
		this.driver.findElement(By.className("search-box__button-cta")).click();
```
