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
    
def get_products_with_ratings_and_images():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # SQL query to retrieve all products with their ratings and images
        query = """
            SELECT p.product_id, p.product_name, p.price, p.description, p.seller_username,
                   AVG(r.rating) AS average_rating, GROUP_CONCAT(pi.image_url) AS images
            FROM Products p
            LEFT JOIN Reviews r ON p.product_id = r.product_id
            LEFT JOIN ProductImages pi ON p.product_id = pi.product_id
            GROUP BY p.product_id
        """

        cursor.execute(query)
        products_data = cursor.fetchall()

        products = []
        for product in products_data:
            product_dict = {
                'product_id': product[0],
                'product_name': product[1],
                'price': float(product[2]),
                'description': product[3],
                'seller_username': product[4],
                'average_rating': float(product[5]) if product[5] is not None else None,
                'images': product[6].split(',') if product[6] is not None else []
            }
            products.append(product_dict)

        cursor.close()
        connection.close()

        return products

    except Exception as e:
        # Log the error or handle it as needed
        raise e