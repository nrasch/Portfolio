package core;

import java.util.concurrent.TimeUnit;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;

/**
 * Concrete implementation of IDriverManager interface for dependency injection.
 * 
 * Creates an instance of the webdriver for local utilization (i.e. non-grid)
 * 
 * @author nathanrasch
 * 
 */
public class LocalDriverManager implements IDriverManager {
	
	private ILogger logger;
	
	
	/**
	 * Initialize class' properties
	 * 
	 * @param logger
	 */
	public LocalDriverManager(ILogger logger) {
		this.logger = logger;
	}

	/**
	 * Instantiate and configure requested webdriver instance and return to calling function
	 * 
	 * @param settings
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
