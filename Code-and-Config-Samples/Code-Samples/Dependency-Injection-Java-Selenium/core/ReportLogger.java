package core;

import org.testng.Reporter;

/**
 * Concrete implementation of ILogger interface for dependency injection
 * 
 * @author nathanrasch
 */
public class ReportLogger implements ILogger{
	
	private StackTraceElement[] stackTraceElements;
	private String className;

	/**
	 * Use the org.testng.Reporter to "log" messages sent to the function by external sources
	 * (These show up in the TestNG reports and XML...)
	 * 
	 * @param message
	 */
	@Override
	public void log(String message) {
		// pull the name of the class calling the log method
		this.stackTraceElements = Thread.currentThread().getStackTrace();
		this.className = stackTraceElements[2].getClassName();
		
		//write log message prefixed by calling class
		Reporter.log(this.className + " :: " + message);	
	}

}
