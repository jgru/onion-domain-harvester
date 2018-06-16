# onion-domain-harvester
The onion-domain-harvester is a python tool to harvest onion domains and store them in a SQL DB. Onion domains are scraped from
* hiddenwiki
* deepdotweb
the resulting data, which consists of url, their title, a short description, first seen and last seen timestampts, is  stored in a lightweight sqlite database. The tool should run on a daily basis via cronjob.

The resulting database may be useful for assessing digital exhibits, so that darknet markets and other artifacts could be identified and classified, even when they are not accessible anymore. 

## Dependencies
Python packages 
* urllib
* cfscrape
* beautifulsoup
* sqlalchemy

Other dependencies
* tor
