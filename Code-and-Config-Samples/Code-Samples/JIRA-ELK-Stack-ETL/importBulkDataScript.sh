#!/bin/sh

# Clean up from last execution
rm /home/nathanrasch/Dev/Issues/*.csv
rm /home/nathanrasch/Dev/Issues/*.json
rm /home/nathanrasch/Dev/Issues/importResults.txt;

# Pull data from JIRA instance via CLI
/home/nathanrasch/Dev/Issues/jira-cli-5.6.0/jira.sh --action getIssueList --search "project IN ('PROJECTXYZ','Master Project Board') AND createdDate > \"2016/07/18\"" --user "SOMEUSER" --password "SOMEPASSWORD" --server "SOMESERVER" --file "/home/nathanrasch/Dev/Issues//issues.csv" --outputFormat 999 --columns "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87" --dateFormat "yyyy-MM-dd"

# Call the PHP CSV -> JSON script
cd /home/nathanrasch/Dev/Issues
php /home/nathanrasch/Dev/Issues/bulkJSONv2.php

# Remove and create the ES Issues index
curl -XDELETE 'localhost:9900/issues?pretty';
curl -XPUT localhost:9900/issues?pretty -d '{
      "mappings" : {
      "issues" : {
        "properties" : {
          "Account" : {
            "type" : "string","index": "not_analyzed"
          },
          "Affects Version Ids" : {
            "type" : "string","index": "not_analyzed"
          },
          "Affects Versions" : {
            "type" : "string","index": "not_analyzed"
          },
          "Aggregate Current Estimate" : {
            "type" : "string","index": "not_analyzed"
          },
          "Aggregate Original Estimate" : {
            "type" : "string","index": "not_analyzed"
          },
          "Aggregate Time Spent" : {
            "type": "integer"
          },
          "Approvals" : {
            "type" : "string","index": "not_analyzed"
          },
          "Assignee" : {
            "type" : "string","index": "not_analyzed"
          },
          "Business Value" : {
            "type" : "string","index": "not_analyzed"
          },
          "Company Name" : {
            "type" : "string","index": "not_analyzed"
          },
          "Component Ids" : {
            "type" : "string","index": "not_analyzed"
          },
          "Components" : {
            "type" : "string","index": "not_analyzed"
          },
          "Created" : {
            "type":"date","format":"yyyy-MM-dd"
          },
          "Current Estimate" : {
            "type" : "string","index": "not_analyzed"
          },
          "Customer Request Type" : {
            "type" : "string","index": "not_analyzed"
          },
          "Description" : {
            "type" : "string","index": "not_analyzed"
          },
          "Due" : {
            "type":"date","format":"yyyy-MM-dd"
          },
          "Environment" : {
            "type" : "string","index": "not_analyzed"
          },
          "Epic Color" : {
            "type" : "string","index": "not_analyzed"
          },
          "Epic Link" : {
            "type" : "string","index": "not_analyzed"
          },
          "Epic Name" : {
            "type" : "string","index": "not_analyzed"
          },
          "Epic Status" : {
            "type" : "string","index": "not_analyzed"
          },
          "Epic/Theme" : {
            "type" : "string","index": "not_analyzed"
          },
          "Fix Version Ids" : {
            "type" : "string","index": "not_analyzed"
          },
          "Fix Versions" : {
            "type" : "string","index": "not_analyzed"
          },
          "Flagged" : {
            "type" : "string","index": "not_analyzed"
          },
          "Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Iteration" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture Browser" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture Document Mode" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture Operating System" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture Screen Resolution" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture URL" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture User Agent" : {
            "type" : "string","index": "not_analyzed"
          },
          "JIRA Capture jQuery Version" : {
            "type" : "string","index": "not_analyzed"
          },
          "Key" : {
            "type" : "string","index": "not_analyzed"
          },
          "Labels" : {
            "type" : "string","index": "analyzed"
          },
          "Link Directional Names" : {
            "type" : "string","index": "not_analyzed"
          },
          "Link Directions" : {
            "type" : "string","index": "not_analyzed"
          },
          "Link Ids" : {
            "type" : "string","index": "not_analyzed"
          },
          "Link Keys" : {
            "type" : "string","index": "not_analyzed"
          },
          "Link Names" : {
            "type" : "string","index": "not_analyzed"
          },
          "Link Type Ids" : {
            "type" : "string","index": "not_analyzed"
          },
          "MLA" : {
            "type" : "string","index": "not_analyzed"
          },
          "Organizations" : {
            "type" : "string","index": "not_analyzed"
          },
          "Original Estimate" : {
            "type" : "string","index": "not_analyzed"
          },
          "Paid" : {
            "type" : "string","index": "not_analyzed"
          },
          "Parent" : {
            "type" : "string","index": "not_analyzed"
          },
          "Parent Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Parent Link" : {
            "type" : "string","index": "not_analyzed"
          },
          "Priority" : {
            "type" : "string","index": "not_analyzed"
          },
          "Priority Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Project" : {
            "type" : "string","index": "not_analyzed"
          },
          "Project Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Raised During" : {
            "type" : "string","index": "not_analyzed"
          },
          "Rank" : {
            "type" : "string","index": "not_analyzed"
          },
          "Report Types" : {
            "type" : "string","index": "not_analyzed"
          },
          "Reporter" : {
            "type" : "string","index": "not_analyzed"
          },
          "Request participants" : {
            "type" : "string","index": "not_analyzed"
          },
          "Requested On" : {
            "type" : "string","index": "not_analyzed"
          },
          "Requester" : {
            "type" : "string","index": "not_analyzed"
          },
          "Required By" : {
            "type" : "string","index": "not_analyzed"
          },
          "Resolution" : {
            "type" : "string","index": "not_analyzed"
          },
          "Resolution Date" : {
            "type":"date","format":"yyyy-MM-dd"
          },
          "Resolution Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Satisfaction" : {
            "type" : "string","index": "not_analyzed"
          },
          "Satisfaction date" : {
            "type" : "string","index": "not_analyzed"
          },
          "Security Level" : {
            "type" : "string","index": "not_analyzed"
          },
          "Security Level Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Send To" : {
            "type" : "string","index": "not_analyzed"
          },
          "Sprint" : {
            "type" : "string","index": "not_analyzed"
          },
          "Status" : {
            "type" : "string","index": "not_analyzed"
          },
          "Status Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Story Points" : {
            "type": "long"
          },
          "Subtasks" : {
            "type" : "string","index": "not_analyzed"
          },
          "Summary" : {
            "type" : "string","index": "not_analyzed"
          },
          "Team" : {
            "type" : "string","index": "not_analyzed"
          },
          "Test Sessions" : {
            "type" : "string","index": "not_analyzed"
          },
          "Testing Status" : {
            "type" : "string","index": "not_analyzed"
          },
          "Time Spent" : {
            "type": "integer"
          },
          "Time Spent (hrs)" : {
            "type": "integer"
          },
          "Time to resolution" : {
            "type" : "string","index": "not_analyzed"
          },
          "Type" : {
            "type" : "string","index": "not_analyzed"
          },
          "Type Id" : {
            "type" : "string","index": "not_analyzed"
          },
          "Updated" : {
            "type":"date","format":"yyyy-MM-dd"
          },
          "Vote Count" : {
            "type" : "string","index": "not_analyzed"
          },
          "WO #" : {
            "type" : "string","index": "not_analyzed"
          },
          "Watch Count" : {
            "type" : "string","index": "not_analyzed"
          },
          "[CHART] Date of First Response" : {
            "type":"date","format":"yyyy-MM-dd"
          },
          "[CHART] Time in Status" : {
            "type" : "string","index": "not_analyzed"
          },
          "development" : {
            "type" : "string","index": "not_analyzed"
          },
          "Resolution Time" : {
            "type": "integer"
          }
        }
      }
    }
}';

# Load the JIRA data into ES for consumption by Kibana
curl -XPOST 'localhost:9900/issues/issues/_bulk?pretty' --data-binary @issues.json >> ./importResults.txt;
