# Project Name
This will create an EC2 Instance in AWS and configure the MYSQL server with a subinterface. It also has the script to manage the DB entry like Insert/delete and query the datas .


## Table of Contents
* [Technologies Used](#technologies-used)
* [Conclusions](#conclusions)

<!-- You can include any other section that is pertinent to your problem -->
### Technologies-used

       1. Terraform : 1.52
       2. Python    : 3.9

## General Information
1. Setup an AWS server running either CentOS or Rocky Linux.

1. Download terraform
2.  Set the variable
    *  export AWS_ACCESS_KEY_ID="ACCESSKEY"
	*  export AWS_SECRET_ACCESS_KEY="SECRET KEY"

3.  terraform init if needed
4.  terraform plan
5.  terraform apply -auto-approve
6.  Wait for terrafomr to complete the Deployment .
7.  The above will go ahead and deploy a Centos VM and configure the below . This will output the Public IP of the VM that you can connect and also the Endpoint for the API URL ( Wait for 3 minutes or so before you try accessing as it is  he API configuration still being configured in the backend )

         * Install python39 and Jq
         * Install the python module required i.e fastapi/uvicorn/mysql-connector-python/requests and  tabulate
         * Install the mysql community edition
         * Dropping drop cache to clear the memory as it is only 2 GB free tier
         * Mask the native  mysql rpm from the BaseOS
         * Install mysql-community-server
         * Start the mysql service and capture the data that it is listening on alll the ports 
         * Change the password to a known password for root
         * Setup an account toweruser with full privilege 
         * Setup an account towerreadonly with readonly acces . I am using in the FASTAPI to query as it is PoC I hard coded . We could use the vault solution or crypt it in script as well . You can check that using the “SHOW GRANTS FOR 'towerro'@'%';” 
         * Application setup like chaning permission and starting/bootstrapping the FAST API
    
   9. ssh -i /Users/monu/.ssh/towerkeypair centos@<publicip reported from terraform apply
   10. tail -f / var/log/aws_install.log – This should have the
   11. ps -ef | grep app | grep -v grep . This will make sure FASTAPI is up and running
   12. ss -lt | grep mysql -> will be listening on all the interfaces
		
	

    


