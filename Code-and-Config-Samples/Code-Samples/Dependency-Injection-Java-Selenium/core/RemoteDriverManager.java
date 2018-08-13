package core;

import java.util.concurrent.TimeUnit;

import org.openqa.selenium.Platform;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.ie.InternetExplorerDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import java.net.MalformedURLException;
import java.net.URL;
import org.openqa.selenium.remote.RemoteWebDriver;

public class RemoteDriverManager implements IDriverManager {
	
	private ILogger logger;
	
	public RemoteDriverManager(ILogger logger) {
		this.logger = logger;
	}

	public WebDriver getDriver(Settings settings) throws MalformedURLException  {
		this.logger.log("Requested driver: " + settings.getBrowser());
		
		WebDriver driver;
		
		if (settings.getBrowser().equalsIgnoreCase("ie")) {
			driver = new InternetExplorerDriver();
		} else {
			DesiredCapabilities capabilities = DesiredCapabilities.firefox();
			capabilities.setBrowserName("firefox");
			capabilities.setPlatform(Platform.WINDOWS);
			
			driver = new RemoteWebDriver(new URL("SOME-URL"), capabilities);
		}
		
		// set global, Implicit Wait for the driver - http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#implicit-waits
		driver.manage().timeouts().implicitlyWait(settings.getImplicitlyWait(), TimeUnit.SECONDS);
		// maxmize browser window
		driver.manage().window().maximize();
		
		this.logger.log("Driver created.  Returning driver object to calling entity.");
		
		return driver;
	}
}
