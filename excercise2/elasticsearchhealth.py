#Using library requests and os
import requests
import os.path

#Check if file exists
if os.path.isfile("./publicip.txt"):
    #Getting IP of elasticsearch from ansible output file
    ip=open("publicip.txt").readline().rstrip()

    #Forming URL for elasticsearch health
    url="http://" + ip + ":9200/_cluster/health"
    
    #Requesting the elasticsearch health
    try:
       request_output=requests.get(url, timeout=1)
       eshealth=request_output.json()
       print ("Cluster health of name " + eshealth["cluster_name"] + " is " + eshealth["status"].upper())
    #Throw exception is url not found
    except:
       print ("Cluster with IP " + ip + " is not running")
else:
    print ("VM has not been created. Run ansible playbook to create publicip.txt file.")
