# JIRA ELK Stack ETL

## Background and discussion

I needed a *quick and dirty* way to extract data from JIRA, load it into Elasticsearch, and then create a metrics dashboard with Kibana.  The canned JIRA reports just weren't cutting it, and I wanted to leverage the power of Elasticsearch and Kibana while performing custom modifications on several of the JIRA data columns.

Is this code the most elegant, optimized, and ready for massive enterprise distribution ever written?  No. 

Did it serve its purpose, and help me impress upper management in a matter of hours?  Yes.  

Mission accomplished.  :)


### A few tools I utilized
* In order to pull the data out of JIRA I utilized a JIRA Command Line Interface (CLI), which can be found [here](https://marketplace.atlassian.com/plugins/org.swift.jira.cli/versions)
* You can also find a number of examples of how to utilize the JIRA CLI [here](https://bobswift.atlassian.net/wiki/display/JCLI/Examples)
* I also needed to parse the CSV file the CLI would return, so I used the [PHP CSV library](http://csv.thephpleague.com/) which I'd had previous experience with.

### The flow
+ Init the process by calling 'importBulkDataScript.sh'
+ 'importBulkDataScript.sh' calls the JIRA CLI to download the data from JIRA instance
+ 'bulkJSONv2.php' is called to parse the CSV and format it into Elasticsearch appropriate JSON
+ The 'issues' index is removed, recreated, and then loaded with JIRA instance data

### Final sample dashboard screenshot
Below is a screenshot of one of the final metric dashboards that was created with the data:

![Metric-Dashboard-Sample-1](./Metric-Dashboard-Sample-1.png)




