<?php

$ex_dir = getcwd();
chdir(__DIR__);

$fh = null;

try {

  $OPTIONS = getopt('d:t:f:');
  if (!array_key_exists('d', $OPTIONS) || !is_string($OPTIONS['d'])) { throw new Exception("'d' database parameter is not a string."); }
  if (!array_key_exists('t', $OPTIONS) || !is_string($OPTIONS['t'])) { throw new Exception("'t' database parameter is not a string."); }
  if (!array_key_exists('f', $OPTIONS) || !is_string($OPTIONS['f'])) { throw new Exception("'f' database parameter is not a string."); }
  define('DBNAME', $OPTIONS['d']);

  require('../scripts_bootstrap.inc.php');

  // Setup and checek counters
  $offset = 0;
  $limit = 1000;
  $count = (int)Globals::$db->query("SELECT COUNT(*) FROM {$OPTIONS['t']}")->fetchColumn();
  if ($count <= 0 ) { throw new Exception("No rows in `{$OPTIONS['d']}`.`{$OPTIONS['t']}`"); }

  // open the file
  $fh = fopen($OPTIONS['f'], 'ab');
  if (!$fh) { throw new Exception("Could not open {$OPTIONS['f']} for writing."); }

  do {
    // We use an offset to prevent ram overage
    $stm = Globals::$db->query("SELECT * FROM {$OPTIONS['t']} LIMIT {$limit} OFFSET {$offset}");
    if (!$stm) { break; } // We don't have a valid statement

    // loop through the records and output each to a line
    while ($row = $stm->fetch(PDO::FETCH_NUM)) {
      fwritecsv($fh, $row);
    }

    // System protection from runaway script if the dump is huge
    usleep(200000);
  } while(($offset += $limit) < $count);


} catch (Exception $e) {
  error_log($e->getMessage()."\n");
}

if (is_resource($fh)) { fclose($fh); }

chdir($ex_dir);

die("done\n\n");


function fwritecsv($handle, $fields, $delimiter = ',', $enclosure = '"', $null = '') {
  // Check if $fields is an array
  if (!is_array($fields)) { return false; }

  // Walk through the data array
  for ($i = 0, $n = count($fields); $i < $n; $i ++) {
    // Make sure the field data is compatible with output
    if (is_bool($fields[$i])) { $fields[$i] = ($fields[$i] === 'true' ? 'TRUE' : 'FALSE'); } // convert Bools to string
    if (is_null($fields[$i])) { $fields[$i] = $null; } // convert nulls to string
    if (!is_scalar($fields[$i])) { $field[$i] = ''; } // Field is not a single value

    if (!is_numeric($fields[$i]) || $delimiter == '.' || strpos($fields[$i], $delimiter) !== false) {
      // Clean up the data so it fits correctly into cells without whitespace issues or enclosure character problems
      $fields[$i] = trim($fields[$i]);
      $search = array($enclosure, "\r\n");
      $replace = array($enclosure.$enclosure, "\n");
      $fields[$i] = $enclosure.str_replace($search, $replace, $fields[$i]).$enclosure;
    }
  }

  // Combine the data array with $delimiter and write it to the file
  $line = implode($delimiter, $fields) . "\r\n";
  fwrite($handle, $line);

  // Return the length of the written data
  return strlen($line);
}
