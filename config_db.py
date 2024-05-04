import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="shopnest"
        )
        return connection
    except Error as e:
        print("Error connecting to database:", e)
        return None