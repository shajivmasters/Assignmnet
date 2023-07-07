from fastapi import FastAPI
import subprocess
import os
import logging
import mysql.connector


description = """
Tower API

You will be able to:

* **/ping**&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;   &nbsp; &nbsp; : &nbsp; &nbsp; Respond with a pong if the API is live.
* **/configure_sql** &nbsp;:&nbsp; &nbsp; This will create a Subinterface and Bind the DB to the new interface and configure a template DB. This is just a PoC.
* **/getdata** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; :&nbsp; &nbsp; Query the data in the database and return. It can return "DB connection Failed/Data/Empty Table".
"""

app = FastAPI(
    title="Tower API",
    description=description,
    version="0.0.1",
    docs_url = "/swagger",
    redoc_url = "/redoc"
)

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler("fastapi.log")
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

mysql_config = {
        'host': '10.123.1.25',
        'database' : 'tower',
        'user'     : 'towerro',
        'password' : 'Readonly123@',
      }


def execute_query(query):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error executing query: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    statuscode = process.returncode
    logger.debug("Status Code : {} ; Stdout : {} ; stderr : {}".format(statuscode,stdout,stderr))
    return (statuscode,stdout,stderr)

def create_db():
    import mysql.connector
    from mysql.connector import Error
    from datetime import datetime
    logger.debug(f"Creating DB")

    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
            host='10.123.1.25',
            user='toweruser',
            password='Toweruser123@'
        )

    logger.debug(connection)
    # Create a new database
    cursor = connection.cursor(buffered=True)
    cursor.execute('CREATE DATABASE IF NOT EXISTS tower')
    cursor.execute('USE tower')

    cursor.execute('show tables')
    # Create the 'tower' table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS tower (
            Field1 DATETIME,
            Field2 VARCHAR(255),
            Field3 VARCHAR(255),
            PRIMARY KEY (Field2)
            )
           """
    cursor.execute(create_table_query)

    # Insert the data into the 'tower' table
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (current_date_time, 'jlaide', 'Tower home project for SRE using python')
    logger.debug(data)
    clear_query = "DELETE FROM tower"
    cursor.execute(clear_query)
    insert_query = "INSERT INTO tower (Field1, Field2, Field3) VALUES (%s, %s, %s)"
    logger.debug(insert_query)
    cursor.execute(insert_query, data)
    # Commit the changes
    connection.commit()
    cursor.close()
    connection.close()
    return { "result" : "DB creation completed Successfully"}

@app.get("/ping")
def ping():
    return { "result" : "Pong" }

@app.post("/configure_mysql")
def configure_mysql():
    # Configure the subinterface IP address
    ##cmd = f"ifconfig eth0:0 up"
    cmd = f"ip addr | grep 10.123.1.25/24"
    statuscode,stdout,stderr = execute_command(cmd)
    if statuscode == 0:
        return {"result": f"inteface already configured{stderr.decode()}"}
    else:
        cmd = f"ip addr add 10.123.1.25/24 dev eth0"
        statuscode,stdout,stderr = execute_command(cmd)
        if  statuscode != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to configure eth0:0: {stderr.decode()}",
            )

    # Configure MySQL to listen on the subinterface IP
    # Stop the MySQL service
    subprocess.run(["systemctl", "stop", "mysqld"])

    # Edit the MySQL configuration file to bind to the new subinterface
    config_file = "/etc/my.cnf"
    cmd = f"grep  10.123.1.25 /etc/my.cnf"
    statuscode,stdout,stderr = execute_command(cmd)
    if statuscode != 0:
        with open(config_file, "a") as f:
            f.write("\nbind-address = 10.123.1.25\n")
    else:
        logger.debug("Bind address already in the config")

    # Start the MySQL service
    subprocess.run(["systemctl", "start", "mysqld"])

    logger.debug("MySQL configured to listen on the new subinterface.")
    logger.debug("going to create DB")
    #final_result = create_db()
    #print(final_result)
    #return { "result" : "Database tower created successfully!" }
    return create_db()

@app.get("/getdata")
def get_data():
    try:
        query = "SELECT * FROM tower"
        result = execute_query(query)
        logger.debug(result)
        if result:
            return {"result": result}
        else:
            return {"result" : "Empty Table"}
    except:
        return { "result" : "DB connection Failed" }
