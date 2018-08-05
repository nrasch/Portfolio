# Data Export Example Utilizing Bash and PHP

At one point we had a feature in our eletronic data capture (EDC) application to allow users to download extracts of the clinical data on demand.  Most major EDC vendors would charge biopharma companies for this service, but we wanted to give it away as a point of diferentation and for competitive advantage.

## Crontab

The whole thing was kicked by the following `crontab` entry:

```bash
*/10 * * * * bash /var/www/tools/exports/export_processor.sh core
```

## export_processor.sh

The `export_processor.sh' was in charge of processing all the export requests submitted to the system in the GUI.  First it created a `pid` file so we wouldn't have multiple copies running, and then it managed the contents of the `exports` table which tracked all the jobs.  You can see in the code where it moves the jobs through the process and updates each job status.

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

The actual work of extracing the processing the database tables took place in the `FormsExport.sh` file which was called by this line of code:

```bash
/bin/bash /var/www/tools/exports/FormsExport.sh $localDB $fileTag
```

## FormsExport.sh
