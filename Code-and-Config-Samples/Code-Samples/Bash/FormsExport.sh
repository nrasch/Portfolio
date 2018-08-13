#!/bin/bash

# Local database to extract tables tables from
localdb=$1
fileTag=$2

# Directory where non-zipped files will be saved.
BASE_EXPORT_DIR="/var/www/app/exports"
if [ ! -d $BASE_EXPORT_DIR ]; then
  mkdir -p $BASE_EXPORT_DIR
  chmod -R 777 $BASE_EXPORT_DIR
fi

# The working dump directory which will be deleted after all exported data files are zipped
EXPORT_WORKING_DIR="${BASE_EXPORT_DIR}/${fileTag}"
echo "Checking ${EXPORT_WORKING_DIR} diretory..."
if [ ! -d $EXPORT_WORKING_DIR ]; then
  echo "Creating ${EXPORT_WORKING_DIR} diretory..."
  mkdir -p $EXPORT_WORKING_DIR
fi
cd $EXPORT_WORKING_DIR

# These tables may not be downloaded.
blacklist=(
adverse_event_visit_forms
alert_types
...
...
...
visit_domains
visit_domains_visit_kinds
visit_form_type_users
visit_kind_forms
visit_kinds
visits
)

# Test if an array contains an element
array_contains () {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
  return 1
}

# Pull all the tables names for the given database and loop through them
mysql -u root -p'********' -s -e "SELECT table_name FROM information_schema.tables WHERE table_schema='${localdb}'" | while read table

do
  # Skip tables in the black list
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
