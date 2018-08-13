#!/bin/bash

localDB=$1

# Pidfile denotes this script is already running and should not be called again this interval
pidfile="/var/www/tools/exports/${0##*/}.pid"

if [ -e $pidfile ]; then
  echo -e "$0 is already executing.\n"
  exit 1
fi
echo "Beginning exports processing (pid $$ in ${pidfile})..."
echo $$ > $pidfile
mysql -u 'root' -p'********' $localDB -s -e "SELECT export_type, MIN(id) FROM exports WHERE export_status='PENDING' AND pid IS NULL GROUP BY export_type"| while read export_type id
do
    echo "Processing ${export_type} export ${id}..."
    dateTag=`date +%Y%m%d%H%M%S`
    fileTag="${export_type}-${dateTag}"
    mysql -u 'root' -p'********' $localDB -e "UPDATE exports SET export_status = 'RUNNING', started = NOW(), pid = $$ WHERE id = ${id}"

    # ToDo: Switch case for different export_type values
    /bin/bash /var/www/tools/exports/FormsExport.sh $localDB $fileTag

    if [ -f "/var/www/app/exports/${fileTag}.zip" ]; then
      mysql -u 'root' -p'********' $localDB << EOSQL
UPDATE exports SET file_name = '${fileTag}.zip', export_status = 'COMPLETE', ended = NOW() WHERE id = ${id};
DELETE FROM exports WHERE export_type='${export_type}' AND export_status='PENDING' AND pid IS NULL;
EOSQL
   else
      mysql -u 'root' -p'********' $localDB << EOSQL
UPDATE exports SET export_status = 'ERROR', ended = NOW() WHERE id = ${id};
EOSQL
  fi
done

echo -e "Processing finished.\n\n"
rm -f $pidfile
