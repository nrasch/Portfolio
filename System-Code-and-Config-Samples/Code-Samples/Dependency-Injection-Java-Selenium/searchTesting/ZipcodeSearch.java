package searchTesting;

import org.testng.annotations.Test;

import core.ABaseTestingClass;
import core.ILogger;
import core.Settings;

import org.testng.Assert;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import org.apache.commons.lang3.StringUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;


/**
 * Suite of tests for zip code based searches
 * 
 * @author nathanrasch
 *
 */
public class ZipcodeSearch extends ABaseTestingClass{
	private HashMap<String, String> zipcode;
	HashMap<String, Integer> results;
	private Boolean err;
	private HashMap<String, String> badDataPoints;
	
	/**
	 * Initialize object variables
	 * 
	 * @param logger
	 * @param settings
	 * @param zipcode
	 */
	public ZipcodeSearch(ILogger logger, Settings settings, HashMap<String, String> zipcode) {
		this.zipcode = zipcode;
		this.logger = logger;
		this.settings = settings;
		
		// define what "bad" data points look like
		this.badDataPoints = new HashMap<String, String>();
		this.badDataPoints.put(" 0bd/", "0 bedrooms.  ");
		this.badDataPoints.put("/0ba,", "0 bathrooms.  ");
		this.badDataPoints.put(" 0 Sqft,", "0 sq/ft.  ");
	}

	/**
	 * Search by zip code(s), test/validate returned data, and report testing results
	 * 
	 * @throws InterruptedException
	 */
	@Test
	public void searchByZipcode() throws InterruptedException {
		// init vars
		Boolean isPresent;
		Boolean err = true;
		String elementText;
		WebElement pageElement;
		
		this.logger.log("Searching for zipcode " + this.zipcode.get("zip"));
		
		// search for zipcode
		this.driver.findElement(By.id("input-location")).sendKeys(this.zipcode.get("zip"));
		this.driver.findElement(By.className("search-box__button-cta")).click();
		
		// results were found
		isPresent = this.driver.findElements(By.xpath("//div[@class=\"list-view-results\"]/span/span")).size() > 0;
		if (isPresent) {
			pageElement = this.driver.findElement(By.xpath("//div[@class=\"list-view-results\"]/span/span"));
			elementText = pageElement.getText();
			this.logger.log("Zipcode search results: " + elementText);
			err = false;
		}
				
		// no results were found
		elementText = this.driver.findElement(By.id("list-view-container")).getText();
		if (elementText.contains("We could not find properties with the criteria you provided.")) {
			this.logger.log("Zipcode search results: No properties found");
			err = false;
		}
		
		// page didn't load correctly and/or other error
		Assert.assertFalse(err, "Zipcode search results message not found on page");
	}
	
	/**
	 * Loop through the search result items and look for incorrect data points and/or missing images
	 * If found sum how many were found on the page and report findings
	 * 
	 * @throws InterruptedException
	 */
	@Test 
	public void validateZipcodeSearchData() throws InterruptedException {
		// init vars
		this.err = false;
		this.results = new HashMap<String, Integer>();
		Integer missingImageCount = 0;
		
		this.logger.log("Validating zipcode search data for " + this.zipcode.get("zip"));
		
		// search for zipcode
		this.driver.findElement(By.id("input-location")).sendKeys(this.zipcode.get("zip"));
		this.driver.findElement(By.className("search-box__button-cta")).click();
		
		// results were found
		if (this.driver.findElements(By.xpath("//div[@class=\"list-view-results\"]/span/span")).size() > 0) {
			// if zero values are found in results data we should fail
			this.logger.log("Checking list-view-item content data for zero values and/or missing images");
			
			// look for bad data points in the listing items and report outcome
			this.checkDataPoints();
			
			// we should also record and fail missing thumb nail images
			missingImageCount = this.driver.findElements(By.xpath("//img[@src='/img/missing-thumb.png']")).size();
			if (missingImageCount > 0) {
				this.logger.log("Failure.  Page contained " + missingImageCount.toString() + " entries with missing image(s).");
				this.err = true;
			}
			
			// and finally, fail the test if we found bad data on the page
			Assert.assertFalse(this.err,"Data validation failure.  " + this.zipcode.get("zip") + " page contained one or more zero data values.");
			
		} else {
			this.logger.log("Skipping zipcode search data validation.  No properties found for " + this.zipcode.get("zip"));
		}
	}
	
	/**
	 * Look for incorrect data points, sum how many were found, and report results
	 */
	private void checkDataPoints() {
		WebElement pageElement = null;
		
		pageElement = this.driver.findElement(By.id("list-view-container"));
		
		for(Map.Entry<String, String> mentry : this.badDataPoints.entrySet()) {
	         String str = pageElement.getText();
	         String findStr = mentry.getKey().toString();
	         int failCount = StringUtils.countMatches(str, findStr);
	         
	         // record the number of type of bad data points
	         if (failCount > 0) {
	        	 try {
	        		 int count = this.results.get(mentry.getValue()) + failCount;
	        		 this.results.put(mentry.getValue(), count);
	        	 } catch(java.lang.NullPointerException ex) {
	        		 this.results.put(mentry.getValue(), failCount);
	        	 }
	        	 // we found at least one bad data point on the page; the test has failed
	        	 this.err = true;
	         }
		}
		
		// report the number of times we found bad data on the page by test condition to the user
		for(Map.Entry<String, Integer> entry : this.results.entrySet()) {
		    String key = entry.getKey();
		    Integer value = entry.getValue();
		    this.logger.log("Failure.  Page contained " + value.toString() + " entries with " + key);
		}	
	}
}
