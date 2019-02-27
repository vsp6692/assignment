#Using dependncy Libraries
import adal
import requests
import os
import json
import yaml
import datetime

#Getting Resource Values
with open("./group_vars/all.yaml", 'r') as stream:
    try:
        resource_dict=yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#Get Environment variables for Azure Authentication
tenant = os.environ['AZURE_TENANT']
client_id = os.environ['AZURE_CLIENT_ID']
client_secret = os.environ['AZURE_SECRET']
resource = 'https://management.azure.com/'
authority_url = 'https://login.microsoftonline.com/' + tenant

#Get Timespan
endDateTime_ISO=datetime.datetime.utcnow() - datetime.timedelta(minutes=2)
startDateTime_ISO=datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
timespan=startDateTime_ISO.strftime("%Y-%m-%dT%H:%M:%SZ") + "/" + endDateTime_ISO.strftime("%Y-%m-%dT%H:%M:%SZ")

#Get Access Token
context = adal.AuthenticationContext(authority_url)
token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
params = {'api-version': '2018-10-01'}

#Get VM Metrics
print ("------------------------------------------------------------")
print ("VM Name  |  CPU Percentage  |  Disk Usage  |  Network Usage")
print ("------------------------------------------------------------")
for vmname in resource_dict["vm"]:

    #Framing request URL's
    cpu_url = 'https://management.azure.com/subscriptions/'+ os.environ['AZURE_SUBSCRIPTION_ID'] + '/resourceGroups/' + resource_dict["resourcegroup"]["name"] + '/providers/Microsoft.Compute/virtualMachines/' + vmname["name"] + '/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames=Percentage%20CPU&timespan=' + timespan
    network_in_url = 'https://management.azure.com/subscriptions/'+ os.environ['AZURE_SUBSCRIPTION_ID'] + '/resourceGroups/' + resource_dict["resourcegroup"]["name"] + '/providers/Microsoft.Compute/virtualMachines/' + vmname["name"] + '/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames=Network%20In&timespan=' + timespan
    network_out_url = 'https://management.azure.com/subscriptions/'+ os.environ['AZURE_SUBSCRIPTION_ID'] + '/resourceGroups/' + resource_dict["resourcegroup"]["name"] + '/providers/Microsoft.Compute/virtualMachines/' + vmname["name"] + '/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames=Network%20Out&timespan=' + timespan
    disk_read_url = 'https://management.azure.com/subscriptions/'+ os.environ['AZURE_SUBSCRIPTION_ID'] + '/resourceGroups/' + resource_dict["resourcegroup"]["name"] + '/providers/Microsoft.Compute/virtualMachines/' + vmname["name"] + '/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames=Disk%20Read%20Bytes&timespan=' + timespan
    disk_write_url = 'https://management.azure.com/subscriptions/'+ os.environ['AZURE_SUBSCRIPTION_ID'] + '/resourceGroups/' + resource_dict["resourcegroup"]["name"] + '/providers/Microsoft.Compute/virtualMachines/' + vmname["name"] + '/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames=Disk%20Write%20Bytes&timespan=' + timespan

    #Requesting for the Metrics
    cpu_request = requests.get(cpu_url, headers=headers)
    network_in = requests.get(network_in_url, headers=headers)
    network_out = requests.get(network_out_url, headers=headers)
    disk_read = requests.get(disk_read_url, headers=headers)
    disk_write = requests.get(disk_write_url, headers=headers)

    #Printing the output
    cpu_usage=str(cpu_request.json()["value"][0]["timeseries"][0]["data"][-1]["average"]) + "%"
    disk_usage=str(disk_read.json()["value"][0]["timeseries"][0]["data"][-1]["total"] + disk_write.json()["value"][0]["timeseries"][0]["data"][-1]["total"]) + " Bytes" 
    network_usage=str(network_in.json()["value"][0]["timeseries"][0]["data"][-1]["total"] + network_out.json()["value"][0]["timeseries"][0]["data"][-1]["total"]) + " Bytes"
    print (vmname["name"] + "  |  " + cpu_usage + "  |  " + disk_usage + "  |  " + network_usage )
print ("------------------------------------------------------------")
