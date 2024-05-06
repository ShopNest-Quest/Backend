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
    
def get_products_with_ratings_and_images(location=None):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # SQL query to retrieve products with ratings, images, and filter by seller location
        query = """
            SELECT p.product_id, p.product_name, p.price, p.description, p.seller_username,
                   AVG(r.rating) AS average_rating, GROUP_CONCAT(pi.image_url) AS images, p.stock
            FROM Products p
            LEFT JOIN Reviews r ON p.product_id = r.product_id
            LEFT JOIN ProductImages pi ON p.product_id = pi.product_id
            JOIN Sellers s ON p.seller_username = s.username
        """

        if location:
            query += f" WHERE s.location = '{location}'"

        query += " GROUP BY p.product_id"

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
                'images': product[6].split(',') if product[6] is not None else [],
                'stock': product[7]
            }
            products.append(product_dict)

        cursor.close()
        connection.close()

        return products

    except Exception as e:
        # Log the error or handle it as needed
        raise e


def insert_order(customer_username, product_id, quantity):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        # Insert into Orders table
        cursor.execute("""
            INSERT INTO Orders (customer_username, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (customer_username, product_id, quantity))
        cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
        product_price = cursor.fetchone()[0]
        total_price = product_price * quantity
        connection.commit()
        cursor.close()
        return True, {"message" : "Order added successfully", 'total_price': total_price}

    except Error as e:
        return False, f"Error: {e}"

def get_order_details_by_username(customer_username):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch order details for the given customer_username
        query = """
            SELECT o.order_date, p.product_name, p.price, o.quantity, o.total_price, o.status, i.image_url
            FROM Orders o
            JOIN Products p ON o.product_id = p.product_id
            LEFT JOIN ProductImages i ON p.product_id = i.product_id
            WHERE o.customer_username = %s
        """
        cursor.execute(query, (customer_username,))
        order_details = cursor.fetchall()

        if not order_details:
            return False, "No orders found for this customer"

        # Format the order details response
        formatted_orders = []
        for order in order_details:
            formatted_order = {
                "order_date": order[0],           # Access by index 0
                "product_name": order[1],         # Access by index 1
                "price": float(order[2]),         # Access by index 2
                "quantity": order[3],             # Access by index 3
                "total_price": float(order[4]),   # Access by index 4
                "status": order[5]                # Access by index 5
            }
            if order[6]:  # Check if image_url is not None
                formatted_order["image_url"] = order[6]

            formatted_orders.append(formatted_order)

        cursor.close()
        return True, {'orders': formatted_orders}

    except Error as e:
        return False, f"Error: {e}"

def get_orders_sold_by_seller(seller_username):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch order details for the specified seller_username
        query = """
            SELECT o.order_date, p.product_name, p.price, o.quantity, o.total_price, o.status, i.image_url, p.product_id,o.order_id
            FROM Orders o
            JOIN Products p ON o.product_id = p.product_id
            LEFT JOIN ProductImages i ON p.product_id = i.product_id
            WHERE p.seller_username = %s
        """
        cursor.execute(query, (seller_username,))
        order_details = cursor.fetchall()

        if not order_details:
            return False, "No orders found for this seller"

        # Format the order details response
        formatted_orders = []
        for order in order_details:
            order_date = order[0].strftime('%Y-%m-%d %H:%M:%S')  # Format order_date
            product_name = order[1]
            price = float(order[2])
            quantity = order[3]
            total_price = float(order[4])
            status = order[5]
            product_id = order[7]
            order_id = order[8]

            formatted_order = {
                "order_date": order_date,
                "product_name": product_name,
                "price": price,
                "quantity": quantity,
                "total_price": total_price,
                "status": status,
                "product_id": product_id,
                "order_id" : order_id
            }
            if order[6]:  # Check if image_url is not None
                formatted_order["image_url"] = order[6]

            formatted_orders.append(formatted_order)

        cursor.close()
        return True, formatted_orders

    except Error as e:
        return False, f"Error: {e}"

    
def get_reviews_by_product_id(product_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch reviews for the specified product_id
        query = """
            SELECT r.review_id, r.username, r.rating, r.comment, r.review_date
            FROM Reviews r
            JOIN Users u ON r.username = u.username
            WHERE r.product_id = %s
        """
        cursor.execute(query, (product_id,))
        reviews = cursor.fetchall()

        if not reviews:
            return False, "No reviews found for this product"

        # Format the review details response
        formatted_reviews = []
        for review in reviews:
            formatted_review = {
                "review_id": review[0],
                "username": review[1],
                "rating": review[2],
                "comment": review[3],
                "review_date": review[4].strftime('%Y-%m-%d %H:%M:%S')
            }
            formatted_reviews.append(formatted_review)

        cursor.close()
        return True, formatted_reviews

    except Error as e:
        return False, f"Error: {e}"

def change_order_status(order_id, new_status):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Update order status in the Orders table
        update_query = """
            UPDATE Orders
            SET status = %s
            WHERE order_id = %s
        """
        cursor.execute(update_query, (new_status, order_id))
        connection.commit()

        # Check if any rows were affected by the update
        if cursor.rowcount == 0:
            cursor.close()
            return False, f"Order with order_id {order_id} not found"

        cursor.close()
        return True, f"Order status updated to {new_status}"

    except Error as e:
        return False, f"Error: {e}"

def get_products_sold_by_seller(seller_username):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # SQL query to retrieve products sold by the specified seller with ratings and images
        query = """
            SELECT p.product_id, p.product_name, p.price, p.description, p.seller_username,
                   AVG(r.rating) AS average_rating, GROUP_CONCAT(pi.image_url) AS images, p.stock
            FROM Products p
            LEFT JOIN Reviews r ON p.product_id = r.product_id
            LEFT JOIN ProductImages pi ON p.product_id = pi.product_id
            WHERE p.seller_username = %s
            GROUP BY p.product_id
        """

        cursor.execute(query, (seller_username,))
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
                'images': product[6].split(',') if product[6] is not None else [],
                'stock': product[7]
            }
            products.append(product_dict)

        cursor.close()
        connection.close()

        return True,products

    except Error as e:
        # Log the error or handle it as needed
        return False,f"Error: {e}"
    
def update_product_stock(product_id, new_stock):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Update product stock in the Products table
        update_query = """
            UPDATE Products
            SET stock = %s
            WHERE product_id = %s
        """
        cursor.execute(update_query, (new_stock, product_id))
        connection.commit()

        # Check if any rows were affected by the update
        if cursor.rowcount == 0:
            cursor.close()
            return False, f"Product with product_id {product_id} not found"

        cursor.close()
        return True, f"Product stock updated to {new_stock}"

    except Error as e:
        return False, f"Error: {e}"

def change_user_blocked_status(username, is_blocked):
    """Change the 'isBlocked' status of a user in the Users table."""
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Update 'isBlocked' status for the specified user
        update_query = """
            UPDATE Users
            SET isBlocked = %s
            WHERE username = %s
        """
        cursor.execute(update_query, (is_blocked, username))
        connection.commit()

        # Check if any rows were affected by the update
        if cursor.rowcount == 0:
            cursor.close()
            return False, f"User with username '{username}' not found"

        cursor.close()
        return True, f"User '{username}' blocked status updated successfully"

    except Error as e:
        return False, f"Error: {e}"
    
def change_seller_blocked_status(username, is_blocked):
    """Change the 'isBlocked' status of a user in the Users table."""
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Update 'isBlocked' status for the specified user
        update_query = """
            UPDATE Sellers
            SET isBlocked = %s
            WHERE username = %s
        """
        cursor.execute(update_query, (is_blocked, username))
        connection.commit()

        # Check if any rows were affected by the update
        if cursor.rowcount == 0:
            cursor.close()
            return False, f"Seller with username '{username}' not found"

        cursor.close()
        return True, f"Seller '{username}' blocked status updated successfully"

    except Error as e:
        return False, f"Error: {e}"

def get_users_or_sellers_with_blocked_status(user_type):
    """Retrieve users or sellers along with their 'isBlocked' status."""
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Determine the query based on user_type ("users" or "sellers")
        if user_type == "users":
            query = """
                SELECT username, isBlocked
                FROM Users
            """
        elif user_type == "sellers":
            query = """
                SELECT username, isBlocked
                FROM Sellers
            """
        else:
            return None  # Invalid user_type

        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    except Error as e:
        print(f"Error retrieving {user_type}: {e}")
        return None

def add_review_to_database(product_id, username, rating, comment):
    """Add a review to the 'reviews' table."""
    try:
        connection = create_connection()
        if connection is None:
            return False, "Failed to connect to database"

        cursor = connection.cursor()
        insert_query = """
            INSERT INTO reviews (product_id, username, rating, comment)
            VALUES (%s, %s, %s, %s)
        """
        review_values = (product_id, username, rating, comment)
        cursor.execute(insert_query, review_values)
        connection.commit()

        cursor.close()
        connection.close()

        return True, "Review added successfully"

    except Error as e:
        return False, f"Error adding review: {e}"
