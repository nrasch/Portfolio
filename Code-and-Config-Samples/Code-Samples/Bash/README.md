# Data Export Example Utilizing Bash and PHP

At one point we had a feature in our electronic data capture (EDC) application to allow users to download extracts of the clinical data on demand.  Most major EDC vendors would charge biopharma companies for this service, but we wanted to give it away as a point of differentiation and for competitive advantage.

## Crontab

The whole thing was kicked by the following `crontab` entry:

```bash
*/10 * * * * bash /var/www/tools/exports/export_processor.sh core
```

## export_processor.sh

The `export_processor.sh` was in charge of processing all the export requests submitted to the system in the GUI.  First it created a `pid` file so we wouldn't have multiple copies running, and then it managed the contents of the `exports` table which tracked all the jobs.  You can see in the code where it moves the jobs through the process and updates each job status.

Example of a job being marked as in progress:
```bash
echo "Processing ${export_type} export ${id}..."
dateTag=`date +%Y%m%d%H%M%S`
fileTag="${export_type}-${dateTag}"
mysql -u 'root' -p'********' $localDB -e "UPDATE exports SET export_status = 'RUNNING', started = NOW(), pid = $$ WHERE id = ${id}"
```

Example of a job being marked as complete:
```bash
mysql -u 'root' -p'********' $localDB << EOSQL
    UPDATE exports SET export_status = 'ERROR', ended = NOW() WHERE id = ${id};
EOSQL
```

The actual work of extracting and processing the database tables took place in the `FormsExport.sh` file which was called by this line of code:

```bash
/bin/bash /var/www/tools/exports/FormsExport.sh $localDB $fileTag
```

## FormsExport.sh

The forms export script did all the actual work of talking to the database, pulling the data, formatting it, and then writing the results into an archive the user could download.

The first thing the script did was ensure the required export directory structure existed:

```bash
# Directory where non-zipped files will be saved.
BASE_EXPORT_DIR="/var/www/app/exports"
if [ ! -d $BASE_EXPORT_DIR ]; then
  mkdir -p $BASE_EXPORT_DIR
  chmod -R 777 $BASE_EXPORT_DIR
fi

# The working dump directory which will be deleted after all exported data files are zipped
EXPORT_WORKING_DIR="${BASE_EXPORT_DIR}/${fileTag}"
echo "Checking ${EXPORT_WORKING_DIR} directory..."
if [ ! -d $EXPORT_WORKING_DIR ]; then
  echo "Creating ${EXPORT_WORKING_DIR} directory..."
  mkdir -p $EXPORT_WORKING_DIR
fi
cd $EXPORT_WORKING_DIR
```

Next a blacklist of tables we *didn't* want to export was defined on line 24.

```bash
blacklist=(
    adverse_event_visit_forms
    alert_types
    etc.
    etc.
```

Once that was done a list of tables in the given database was acquired, and then this list was iterated over and processed for data extraction:

```bash
do
  # Skip tables in the blacklist
  if ! array_contains $table "${blacklist[@]}" ; then
    # Get column list, awk off first column, convert to comma delimiter, and remove trailing comma.
    echo "Exporting ${table}..."
    mysql -u root -p'********' $localdb -e "SHOW columns FROM ${table}" | awk '{if (NR>1) {print $1;}}' | perl -pe '(eof)?s/\s+$//:s/\s+$/,/' > $EXPORT_WORKING_DIR/$table.csv
    echo "\r\n" >> $EXPORT_WORKING_DIR/$table.csv
    # Output the table to the CSV file with headers using Append mode in PHP
    # PHP script used here to overcome some CSV compatibility issues with MySQL's data output
    /usr/bin/php /var/www/tools/exports/dumptable.php -d"${localdb}" -t"${table}" -f"${EXPORT_WORKING_DIR}/${table}.csv"
    sed -i 's/\b\([0-9]\{2\}\|UNK\)-\([0-9]\{2\}\|UNK\)-\([0-9]\{4\}\|UNK\)/\2\/\1\/\3/g' "${table}.csv"
    sed -i 's/\\N//g' "${table}.csv"
    sed -i 's/"--"/""/g' "${table}.csv"
    # Change "x/y" numbers to " x/y" so that excel doesn't format them to dates
    sed -i 's/\b\([0-9]\+\)\/\([0-9]\+\)/ \1\/\2/g' "${table}.csv"

    if [ $table == 'SUBWD_forms' ] || [ $table == 'VITAL_forms' ] ; then
      # Remove erroneous html from the csv
      sed -i 's/<[a-zA-Z]\+ *\/>//g' "${table}.csv"
      sed -i 's/<[a-zA-Z]\+ *>//g' "${table}.csv"
      sed -i 's/<\/[a-zA-Z]\+ *>//g' "${table}.csv"
      sed -i 's/&deg;//g' "${table}.csv"
    fi
  fi
done
```

(Note in the code above we make a call to a PHP script, `dumptable.php`.  We'll cover that next.)

Once we had all the data extracted and processed it was time to zip it up for downloading:

```
# Zip contents of data extract directory into ../
cd ..
zipfile="${fileTag}.zip"
echo "Attempting to zip into ${zipfile}..."

if [ -e "${zipDirectory}/${zipfile}" ]; then
  rm -f $zipfile
fi
cd $EXPORT_WORKING_DIR
/usr/bin/zip -r "${BASE_EXPORT_DIR}/${zipfile}" *.csv
chmod -R 777 "${BASE_EXPORT_DIR}/${zipfile}"
echo "Removing ${EXPORT_WORKING_DIR}..."
rm -rf ${EXPORT_WORKING_DIR}
```

##  dumptable.php

The first item of interest this script does is import a file called `scripts_bootstrap.inc.php`.  This was a file included with CakePHP that allowed us to attach to its implementation of PDO for database access.  

Once that was completed we could run the SQL commands to pull the data and write it to file.  Below are some snippets of interest:

```php
// Init vars and confirm args
$offset = 0;
$limit = 1000;
$count = (int)Globals::$db->query("SELECT COUNT(*) FROM {$OPTIONS['t']}")->fetchColumn();
if ($count <= 0 ) { throw new Exception("No rows in `{$OPTIONS['d']}`.`{$OPTIONS['t']}`"); }

// Open the file to write the extracted data into
$fh = fopen($OPTIONS['f'], 'ab');
if (!$fh) { throw new Exception("Could not open {$OPTIONS['f']} for writing."); }

do {
// Utilize an offset to prevent running out of RAM on large extracts
$stm = Globals::$db->query("SELECT * FROM {$OPTIONS['t']} LIMIT {$limit} OFFSET {$offset}");
if (!$stm) { break; } // We don't have a valid statement

// Loop through the records and output each to a line
while ($row = $stm->fetch(PDO::FETCH_NUM)) {
  fwritecsv($fh, $row);
}

// System protection so the we don't have a run away script on large extracts
usleep(200000);
} while(($offset += $limit) < $count);
```

And as seen above once this was complete the calling script performed data processing and final archive creation.
