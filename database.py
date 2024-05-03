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

def check_user_exists(table_name, username):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user is not None
    return False

def register_user(table_name, username, password, email, location=None):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            if location != None:
                query = f"INSERT INTO {table_name} (username, password, email_id, location) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, password, email, location))
                connection.commit()
            else:
                query = f"INSERT INTO {table_name} (username, password, email_id) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, password, email))
                connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print("Error registering user:", e)
            connection.rollback()
            cursor.close()
            connection.close()
    return False
