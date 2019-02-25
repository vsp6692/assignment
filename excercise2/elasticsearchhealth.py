#Using library requests
import requests

#Getting IP of elasticsearch from ansible output file
ip=open("publicip.txt").readline().rstrip()

#Forming URL for elasticsearch health
url="http://" + ip + ":9200/_cluster/health"

#Requesting the elasticsearch health
try:
   request_output=requests.get(url, timeout=1)
   eshealth=request_output.json()
   print ("Cluster health of name " + eshealth["cluster_name"] + " is " + eshealth["status"].upper())

except:
   print ("Cluster with IP " + ip + " is not running")