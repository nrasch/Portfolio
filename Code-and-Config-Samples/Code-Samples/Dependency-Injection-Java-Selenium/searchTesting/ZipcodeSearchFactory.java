package searchTesting;

import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.HashMap;

import org.testng.annotations.Factory;
import org.testng.annotations.Parameters;

import core.DBLogger;
import core.FlatFileLogger;
import core.ILogger;
import core.ReportLogger;
import core.Settings;
import dataSets.ZipCodes;

/**
 * Configures and creates a suite of zipcode tests
 * Provides dependency injection for the test suide objects
 * 
 * @author nathanrasch
 */
public class ZipcodeSearchFactory {
	
	private ILogger logger;
	private Settings settings;
	
	/**
	 * Constructor.  Assign XML config file parameters to settings object, and
	 * create the logging object for dependency injection into testing classes
	 * 
	 * @param logger
	 * @param driverManager
	 * @param browser
	 * @param implicitlyWait
	 * @param baseURL
	 * @throws MalformedURLException
	 */
	@Parameters({"logger", "driverManager", "browser", "implicitlyWait", "baseURL"})
	public ZipcodeSearchFactory(String logger, String driverManager, String browser, Integer implicitlyWait, String baseURL) throws MalformedURLException {
		// define and assign our inversion of control object implementations here
		this.createLogger(logger);
		
		// populuate settings object from XML config file values
		this.settings = new Settings();
		this.settings.setBrowser(browser);
		this.settings.setImplicitlyWait(implicitlyWait);
		this.settings.setDriverManager(driverManager);
		this.settings.setBaseURL(baseURL);
		
		this.logger.log(browser);
		this.logger.log(implicitlyWait.toString());
	}
	
	/**
	 * Configures and creates the array of ZipcodeSearch objects which run the 
	 * required search page zip code tests
	 * 
	 * @return Array of ZipcodeSearch objects
	 */
	@Factory
	public Object[] createInstances() {
		
		// *example for five random zip codes
		//ArrayList<HashMap<String, String>> zipsToTest = ZipCodes.getRandomZipcodes(5);
		
		// *example for two zipcodes: 80905, 10461
		//ArrayList<HashMap<String, String>> zipsToTest = ZipCodes.getStaticZipcodes();
		
		// *example of four zipcodes starting from data source index position 34857 (i.e. Colo Spgs, CO) 
		ArrayList<HashMap<String, Integer>> blockHash = new ArrayList<HashMap<String, Integer>>();
		HashMap<String, Integer> block = new HashMap<String, Integer>();
		block.put("start", 34857);
		block.put("end", 34860);
		blockHash.add(block);
		ArrayList<HashMap<String, String>> zipsToTest = ZipCodes.getBlocksOfZipcodes(blockHash);
		
		
		Object[] result = new Object[zipsToTest.size()];
		
		for (int i = 0; i < zipsToTest.size(); i++) {
			result[i] = new ZipcodeSearch(this.logger, this.settings, zipsToTest.get(i));
        }
		return result;
	}
	
	
	/**
	 * Creates correct logging object based on XML config parameters
	 * 
	 * @param logger
	 */
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
	
}
