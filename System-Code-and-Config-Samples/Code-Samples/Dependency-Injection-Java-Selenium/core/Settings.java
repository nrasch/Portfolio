package core;

/**
 * A class of mostly getters and setters to hold the various testing parameters
 * passed in via the XML config file
 * 
 * @author nathanrasch
 *
 */
public class Settings {

	private String browser;
	private Integer implicitlyWait;
	private String driverManager;
	private String baseURL;
	
	public void setBrowser(String browser) {
		this.browser = browser;
	}
	
	public String getBrowser() {
		return this.browser;
	}
	
	public void setImplicitlyWait(Integer implicitlyWait) {
		this.implicitlyWait = implicitlyWait;
	}
	
	public Integer getImplicitlyWait() {
		return this.implicitlyWait;
	}
	
	public void setDriverManager(String driverManager) {
		this.driverManager = driverManager;
	}
	
	public String getDriverManager() {
		return this.driverManager;
	}
	
	public void setBaseURL(String baseURL) {
		this.baseURL = baseURL;
	}
	
	public String getBaseURL() {
		return this.baseURL;
	}
}
