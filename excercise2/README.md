# Excercise 1

Need to create a Linux machines to run elasticsearch as docker container and check its health.

## High Level Approach

1. Creating a machines in Azure Subsription using Ansible Playbook and run docker container inside it.

2. Created python script to get metrics of VM's using their respective API's. Authetication to API's are done using AD service principals.

## Tech Stacks

* Azure AD
* Docker
* Ansible
* Python

## Prerequisites

There are some prerequisites which need to be setup before we start executing the script.

### Azure Subscription

Create a free azure subscription with your details filled by using the [link](https://azure.microsoft.com/en-in/account/).

### Create App Registration in Azure AD 

The intention of this step is to give access to Ansible to create resources in Azure Subscriptions. Follow this [link](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) for app registrations.

### Setting up Machine

We need Ansible and Python in our local machine to start our work. Create a linux based VM in your azure subscription. For our scenario we can use Ubuntu-16.04 with basic configuration is enough to run the below setup. Follow this [link](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal) to create VM.

Once VM is up login into machine to install required packages. Follow below steps to setup the machine.

```
$ sudo apt-get update
$ sudo apt-get install software-properties-common git -y 
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt-get install ansible -y
$ curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py ; python get-pip.py
$ pip install 'ansible[azure]'
$ git clone https://github.com/vsp6692/assignment.git
```

After cloning the repo replace the env.sh file with suitable variables.

```
  export AZURE_CLIENT_ID="Application ID from App registrations"
  export AZURE_SECRET="App registration secret"
  export AZURE_SUBSCRIPTION_ID="Your Azure Subscription ID"
  export AZURE_TENANT="Your current Azure Tenant ID"
```

## Steps to Complete Excercise

1. Source the auth variables from env.sh

```
source env.sh
```

2. Run ansible playbook to create resources

```
ansible-playbook vmcreation.yml
```

3. Run the python script to display CPU Percentage, Disk Usage and Network Usage of two machines we created

```
python get_metrics.py
```

## Folder Structure

Below is the structure of the excercise directory.

```
excercise2
├── README.md                   ---> Documentation.
├── elasticsearchhealth.py      ---> Python script to check health of elasticsearch.
├── env.sh                      ---> File with authentication varibles.
├── group_vars
│   └── all.yaml                ---> Default variables for VM Creation.
├── publicip.txt
├── roles
│   └── azure_vm
│       ├── files
│       │   └── cloud-init.yml  ---> Cloud init file which will be called after VM creation to start docker container.
│       └── tasks
│           └── main.yaml       ---> Playbook for having all tasks to create VM.
└── vmcreation.yaml             ---> Startup playbook.
```