# Nginx Code Sample

## Background
While prototyping and demoing a solution utilizing Elasticsearch (ES) and Kibana we needed a way to restrict access to the Elasticsearch implementation.  The Elasticsearch company wanted $15,000 for a license to provide a security solution.  Since this was a startup needless to say that sort of expenditure wasn't forthcoming until a bolus of paying clients was obtained...

After researching the matter I found some articles about securing Elasticsearch with Nginx, which resulted in the following configuration file.

Goals of the configuration included:
* Allow access over SSL only
* Provide CORS functionality between the external UI server and the API/ES service
* Prevent access to the more destructive/dangerous areas of ES
* Continue to accept and serve RESTFUL calls to the non-ES portion of the API server
* Conform suggested best practices (at that time) for securing the Nginx implementation