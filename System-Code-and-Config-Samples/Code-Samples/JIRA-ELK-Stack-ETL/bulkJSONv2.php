<?php

# Setup CSV lib
require 'vendor/autoload.php';
use League\Csv\Reader;

# Set timezone for date formatting
date_default_timezone_set('America/Denver');

# Set ES index
$index = 'issues';

# Define which JIRA data columns we want to format
$dates = array(
	'Created',
	'Due',
	'Resolution Date',
	'Updated'
);

$numbers = array(
  'Story Points'
);

# Collect CSV files we need to convert
$files = glob('*.{csv}', GLOB_BRACE);

# Process each CSV file
foreach($files as $file) {

  # Create output file based on input file
  $type = basename($file, '.csv');
  echo "Parsing $file\n";
  $outputFile = fopen($type.'.json', "w") or die("Unable to open file!");

  # Instantiate CSV reader
  $csv = Reader::createFromPath($file);
  $data = $csv->setOffset(0)->fetchAssoc();

  # ES JSON header string 'constant'
  $header = '{"create":{"_index":"'.$index.'","_type":"'.$type.'"}}'."\n{";

  # Process each row in the CSV source file
  foreach ($data as $d) {
    $output = $header;

    foreach ($d as $k => $v) {
      $isDate = false;
      $isNum = false;
      
      if (in_array($k, $dates)) {
        $isDate = true;
      }

      if (in_array($k, $numbers)) {     
        $isNum = true;
      }
      
      if ($k == 'Sprint') {
        //Sometimes we get items like this: IA - November 23rd Sprint,IA - December 7th Sprint
        //Need to only use the last entry in the comma seperated list
        $_tmp = explode(',', $v);
        $v = array_pop($_tmp);
        unset($_tmp);
      }
      
      // Format the field's key
      $k = "\"$k\":";
      
      // Format the field's value if empty date
      if ($isDate) {
        if (empty($v)) {
          $v = 'null';
        } 
      }
      
      // Format field's value regardless of data type
      if (empty($v)) {
        $v = '""';
        if ($isNum) {
          $v = 'null';
        }
      } else {
        if ($v != 'null') { 
          if ($isNum) {
            $v = str_replace('"', '', $v);
            $v = str_replace("'", '', $v);
          } else {
            $v = str_replace('"', '\"', $v);
            $v = preg_replace( "/\r|\n/", "", $v );
            $v = "\"$v\"";
          }
        }
      }  
      
	  # Add the JSON key/value pair to the output string
	  $output .= $k.$v.',';
    }
    
    // Calculate how long the issue took to resolve
    $days = 'null';
    if (!empty($d['Created']) && !empty($d['Resolution Date'])) {
        $date1 = new DateTime($d['Created']);
        $date2 = new DateTime($d['Resolution Date']);
        $interval = $date1->diff($date2);
        $days = $interval->days;
    }
    # Add custom JSON key/value pair to the output string
	$output .= "\"Resolution Time\":$days,";

    // Convert Time Spent from seconds to hours
    $timeSpentHours = 'null';
    if (!empty($d['Time Spent'])) {
        $timeSpentHours = number_format($d['Time Spent'] / 3600, 1);;
    }   
	# Add custom JSON key/value pair to the output string
    $output .= "\"Time Spent (hrs)\":$timeSpentHours,";
    
    # Add JSON seperators and terminators
	$output = rtrim($output, ',');
    $footer = "}\n";
    
	# Write JSON row to output file
	fwrite($outputFile, $output.$footer);
  }
  
  # Clean up
  unset($csv);
  fclose($outputFile);
  unset($outputFile);
  
  # We're done with this source file
  echo "Finished writing to $type.json\n";
}

?>
