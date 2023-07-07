# Project Name
This will create an EC2 Instance in AWS and configure the MYSQL server with a subinterface. It also has the script to manage the DB entry like Insert/delete and query the datas .


## Table of Contents
* [Technologies Used](#technologies-used)
* [General Infromation](#general-information)
* [Test Cases](#test-cases)

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

    9.	ssh -i /Users/monu/.ssh/towerkeypair centos@<publicip reported from terraform apply
    10.	tail -f / var/log/aws_install.log – This should have the
    11.	ps -ef | grep app | grep -v grep . This will make sure FASTAPI is up and running
    12.	ss -lt | grep mysql -> will be listening on all the interfaces


3. Create a Python application/script that connects to an API that can : 
Configure a new subinterface (alias interface) and setup an ip/subnet on the new subinterface
Configure MySQL to listen only on the new subinterface
Create a database called 'tower', a table called 'tower' with following data stored in the table:
Field1 | Field2 | Field3
Current date and time | jlaide | Tower home project for SRE

		There is multiple way you can do this 
			Ø Using the FASTAPI directly by accessing using http://<PubIP>/swagger  . The same link will give you the usages. This allows you to query and bootstrap the DB . It is a conscious decision not to provide the update capability for the end user . The Update is provided using the /home/centos/scripts/dbmanage.py insert/delete options in the CLI.If you test the http://<PubIP>/getdata it should through the error “DB connection Failed” 
			Ø Using the script which in turn calling the API to achieve /home/centos/scripts/dbmanage.py create 
			Ø Using a simple Curl POST command curl -X POST http://<PubIP>/configure_mysql
			Ø Using the FASTAPI directly by accessing using http://<PubIP>/ping. You should get a "Pong" response 
3. Your application/script should be able to get all the data from the table and output the data to the screen
   
		You can do this with following ways
			Ø Using the API or curl you can do it "curl -s  http://<PubIP>/getdata" or from the host itself you can run "curl -s http://localhost/getdata | jq "
			Ø /home/centos/scripts/dbmanage.py query -p <password>
		
4. Your application/script should be able to change the data in the table and output the new data to the screen 

		Ø /home/centos/scripts/dbmanage.py insert  -p <password> -f2 <username>  data -f3 <comments> [-f1 <datetime> default <currentdatetime> ]
		As you can see "Fiedl1" set this as optional and if it is not provided it will insert the current date/time 																
		Ø The primary key here is the feild2 <username> and will update the existing entry if it exist if not insert the provided data	
		Ø Query the data 
			Ø Using the API or curl you can do it "curl -s  http://<PubIP>/getdata" or from the host itself you can run "curl -s http://localhost/getdata | jq "
			Ø /home/centos/scripts/dbmanage.py query -p <password>
   		Ø You can delete the entry using /home/centos/scripts/dbmanage.py delete -p <password> -f2 <username> . Note the "Field2" is the primary key 

dbmanage.py sript options


 ![image](https://github.com/shajivmasters/Assignmnet/assets/116799274/4b7d9b2d-a035-40b7-a7e0-7400af17a747)
