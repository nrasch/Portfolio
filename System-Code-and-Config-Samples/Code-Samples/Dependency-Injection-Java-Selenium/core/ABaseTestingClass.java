package core;

import org.testng.annotations.BeforeMethod;

import java.net.MalformedURLException;

import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;

import core.IDriverManager;
import core.ILogger;
import core.Settings;

/**
 * Contains common elements to all test classes
 * 
 * @author nathanrasch
 *
 */
public abstract class ABaseTestingClass {
	protected IDriverManager driverManager;
	protected WebDriver driver;
	protected ILogger logger;
	protected Settings settings;
	
	/**
	 * Before each test create the proper WebDriver and browse to the base testing URL 
	 * 
	 * @throws InterruptedException
	 * @throws MalformedURLException
	 */
	@BeforeMethod
	public void beforeMethod() throws InterruptedException, MalformedURLException {
		this.createDriverManager(this.settings.getDriverManager());
		this.driver.get(this.settings.getBaseURL());
	}

	/**
	 * Clean up the browser after each test is run.
	 */
	@AfterMethod
	public void afterMethod() {
		this.driver.close();
		this.driver.quit();
	}
	
	/**
	 * Instantiates concrete implementation of the IDriverManager interface.
	 * 
	 * (LocalDriverManager is default.)
	 * 
	 * @param driverManager
	 * @throws MalformedURLException
	 */
	protected void createDriverManager(String driverManager) throws MalformedURLException {
		if (driverManager == "RemoteDriverManager") {
			this.driverManager = new RemoteDriverManager(this.logger);
		} else {
			this.driverManager = new LocalDriverManager(this.logger);
		}
		this.driver = this.driverManager.getDriver(this.settings);
	}
	
}
