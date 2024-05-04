from mysql.connector import Error
from config_db import create_connection

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

def add_product_to_db(product_data):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Extract product details from product_data dictionary
        product_name = product_data.get('product_name')
        price = product_data.get('price')
        description = product_data.get('description')
        seller_username = product_data.get('seller_username')
        category_id = product_data.get('category_id', None)
        stock = product_data.get('stock', 0)
        images = product_data.get('images', [])

        # Insert product details into Products table
        insert_query = """
            INSERT INTO Products (product_name, price, description, seller_username, category_id, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (product_name, price, description, seller_username, category_id, stock))
        product_id = cursor.lastrowid  # Get the auto-generated product_id

        # Insert product images into ProductImages table
        for image_url in images:
            insert_image_query = """
                INSERT INTO ProductImages (product_id, image_url)
                VALUES (%s, %s)
            """
            cursor.execute(insert_image_query, (product_id, image_url))

        connection.commit()
        cursor.close()
        connection.close()

        return {"success": True, "message": "Product and images added successfully", "product_id": product_id}

    except Exception as e:
        print("Error adding product:", e)
        return {"success": False, "message": "Failed to add product"}