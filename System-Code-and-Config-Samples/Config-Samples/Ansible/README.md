# Ansible Code Samples

## Directory Structure

```
└───Ansible
    ├───Backups
    │       backupIndices.yml
    │       backupMySQL.yml
    │
    └───Update
        │   updateServer.yml
        │
        └───tasks
                rebootOS.yml
                startKibana.yml
                startKibi.yml
                upgradeOS.yml
```
						
## Backups
Two sample scripts to backup a MySQL server and a set of Elasticsearch indices.  After the backups occur they are zipped to moved off-server to an Amazon S3 storage area.

## Update
A simple set of tasks to apply updates to production servers.  After the server reboots the UI analytics service is started.  Since we were utilizing A/B split testing between server instances we needed to ensure the correct service was started.
