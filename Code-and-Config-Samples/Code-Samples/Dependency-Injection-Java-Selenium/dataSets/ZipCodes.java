package dataSets;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

/**
 * "Static" class
 * Builds a data set of zip codes from an external source (usually CSV from goverment census sources)
 * Return some subset of those zip codes to calling functions (randomly, blocks, staticly defined, etc.)
 * We only want to parse and load the external source once
 * 
 * @author nathanrasch
 */
public final class ZipCodes {
	
	/**
	 * Private constructor, so we have a "static" class 
	 */
	private ZipCodes() {}
	
	/**
	 * Container for the parsed zip code data set 
	 */
	private static ArrayList<HashMap<String, String>> zipCodesList = new ArrayList<HashMap<String, String>>();
	
	/**
	 * @param numberRequested
	 * @return Arraylist of Hashmaps of zip codes randomly pulled from the zip code data set
	 */
	public static ArrayList<HashMap<String, String>> getRandomZipcodes(int numberRequested) {
		ZipCodes.populateZipcodeList();
		
		ArrayList<HashMap<String, String>> resultSet = new ArrayList<HashMap<String, String>>();
		Random randomGenerator = new Random();
		int index;
		
		// pull random # of entries from ZipCodes.zipCodesList based on parameter numberRequested
		for (int i = 0; i < numberRequested; i++) {
			index = randomGenerator.nextInt(ZipCodes.zipCodesList.size());
	        resultSet.add(ZipCodes.zipCodesList.get(index));
		}
		
		return resultSet;
	}
	
	/**
	 * @param blockHash
	 * @return Arraylist of Hashmaps of zip code blocks pulled from the zip code data set
	 */
	public static ArrayList<HashMap<String, String>> getBlocksOfZipcodes(ArrayList<HashMap<String, Integer>> blockHash) {
		ZipCodes.populateZipcodeList();
		
		ArrayList<HashMap<String, String>> resultSet = new ArrayList<HashMap<String, String>>();
		
		// each blockHash should have a 'start' and 'end' integer value we'll use to pull and return blocks of zips out of the master list
		Iterator<HashMap<String, Integer>> iterator = blockHash.iterator();
		
		while(iterator.hasNext()) {
			HashMap<String, Integer> block = iterator.next();
			int start = block.get("start");
			int end = block.get("end");
			for (int i = start; i <= end; i++) {
				resultSet.add(ZipCodes.zipCodesList.get(i));
			}
		}
		
		return resultSet;
    }
	
	/**
	 * @return Arraylist of Hashmaps of zip codes statically defined (ex: quick testing)
	 */
	public static ArrayList<HashMap<String, String>> getStaticZipcodes() {
		ArrayList<HashMap<String, String>> resultSet = new ArrayList<HashMap<String, String>>();
		HashMap<String, String> zip;
		
		zip = new HashMap<String, String>();
		zip.put("zip", "80905");
		resultSet.add(zip);
		
		zip = new HashMap<String, String>();
		zip.put("zip", "10562");
		resultSet.add(zip);
		
		zip = new HashMap<String, String>();
		zip.put("zip", "10708");
		resultSet.add(zip);
		
		return resultSet;
	}
	
	/**
	 * Parses the zip code source data set and loads it into the object for external consumption
	 */
	private static void populateZipcodeList() {
		// only load the data once...
		if (ZipCodes.zipCodesList.size() > 0) {
			return;
		}
		
		List<String> headers = null;
		List<String> values = null;
		String line = null;
		
		// create handle the source data file
		InputStream stream = ZipCodes.class.getResourceAsStream("zipCodes.csv");
		BufferedReader buffer = new BufferedReader(new InputStreamReader(stream));

        try {
			// pull header row
        	headers = Arrays.asList(buffer.readLine().split(","));
        	
        	// add data rows
        	while((line = buffer.readLine()) != null) {
        	
        		HashMap<String, String> zip = new HashMap<String, String>();
        		values = Arrays.asList(line.split(","));
        		for (int i = 0; i < headers.size(); i++) {
        			zip.put(headers.get(i), values.get(i));
        		}
        		ZipCodes.zipCodesList.add(zip);
			}
			stream.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}

}
