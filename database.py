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

def register(table_name, username, password, email, location=None):
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

def authenticate(table_name, username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user_info = cursor.fetchone()  # Fetch a single row
        if user_info:
            # Convert tuple to dictionary for easier access
            if table_name != "Admin":
                user_dict = {
                        'username': user_info[0],
                        'password': user_info[1],
                        'isBlocked': user_info[2],
                        'email_id': user_info[3]
                }
            else:
                user_dict = {
                        'username': user_info[0],
                        'password': user_info[1],
                        'email_id': user_info[2]
                }
            return user_dict
        else:
            return None  
    return None
