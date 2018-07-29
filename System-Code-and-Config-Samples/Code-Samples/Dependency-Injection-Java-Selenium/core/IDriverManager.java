package core;

import java.net.MalformedURLException;
import org.openqa.selenium.WebDriver;

/**
 * Abstraction of the web driver functionality via an Interface definition.
 * 
 * Should be implemented concretely by other classes as passed to target
 * class' constructor via dependency injection.
 * 
 * @author nathanrasch
 */
public interface IDriverManager {
	
	/**
	 * @param settings
	 * @return
	 * @throws MalformedURLException
	 */
	public WebDriver getDriver(Settings settings) throws MalformedURLException;
}
