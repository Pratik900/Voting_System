# import module of mysql connector
import mysql.connector

# create a connection and return it from the function
def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "cdac",
        database = "iotdb",
        use_pure=False 
    )