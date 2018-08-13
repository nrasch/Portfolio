package core;

/**
 * Abstraction of the logging functionality via an Interface definition.
 * 
 * Should be implemented concretely by other classes as passed to target
 * class' constructor via dependency injection.
 * 
 * @author nathanrasch
 */
public interface ILogger {
	
	/**
	 * @param message
	 */
	public void log(String message);
}
