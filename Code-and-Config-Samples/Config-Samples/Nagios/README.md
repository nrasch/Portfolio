# Nagios Code Samples

## Directory Structure

```
├───client
│   ├───nrpe.cfg
│   │       nrpe.cfg
│   │
│   └───plugins
│           check_mem
│
└───server
    ├───etc
    │   ├───objects
    │   │       commands.c
    │   │
    │   └───servers
    │           demo-api.c
    │           demo.cfg
    │
    └───libexec
            check_mem
```
	
## Background
We needed a quick and dirty way to monitor our demo server (among others).  Enter Nagios...

The service was setup on the client machines to monitor items such as:

* Root partition disc space
* Number of users logged into the machine
* Server load
* Zombie processes
* Total processes
* MySQL daemon status
* SSH service availability
* Elasticsearch availability
* API availability
* Memory usage
	
## Client
Sample files that were place on the Nagios client machines.

## Server
Sample files on the Nagios server which polled the clients, reported metrics via the administration web page, etc.