import random
import mysql.connector
from db_functions import create_connection

tables = [
    """
    CREATE TABLE IF NOT EXISTS Categories (
        cat_id INT PRIMARY KEY,
        category_name VARCHAR(50) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Users (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        isBlocked BOOLEAN DEFAULT FALSE,
        email_id VARCHAR(100) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Admin (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        email_id VARCHAR(100) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Sellers (
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        isBlocked BOOLEAN DEFAULT FALSE,
        location VARCHAR(255),
        email_id VARCHAR(100) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        description TEXT,
        seller_username VARCHAR(50) NOT NULL,
        category_id INT,
        stock INT NOT NULL DEFAULT 0,
        FOREIGN KEY (seller_username) REFERENCES Sellers(username),
        FOREIGN KEY (category_id) REFERENCES Categories(cat_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Reviews (
        review_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        username VARCHAR(50) NOT NULL,
        rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
        comment TEXT,
        review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (username) REFERENCES Users(username)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ProductImages (
        image_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        image_url VARCHAR(255) NOT NULL,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_username VARCHAR(50) NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        total_price DECIMAL(12, 2) NOT NULL,
        status ENUM('pending', 'shipped', 'delivered') DEFAULT 'pending',
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_username) REFERENCES Users(username),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )
    """,
    """
    CREATE TRIGGER IF NOT EXISTS before_insert_order
    BEFORE INSERT ON Orders
    FOR EACH ROW
    BEGIN
        DECLARE product_price DECIMAL(10, 2);
        SELECT price INTO product_price FROM Products WHERE product_id = NEW.product_id;
        SET NEW.price = product_price;
        SET NEW.total_price = NEW.price * NEW.quantity;
    END
    """
]


def create_tables():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        # Execute each table creation statement
        for table in tables:
            try:
                cursor.execute(table)
                print("Table created successfully")
            except mysql.connector.Error as err:
                print(f"Error creating table: {err}")

        # Committing the transaction and closing the connection
        connection.commit()
        cursor.close()
        connection.close()


def add_default_categories():
    required_categories = [
        (1, 'Electronics'),
        (2, 'Clothing'),
        (3, 'Books'),
        (4, 'Home & Kitchen'),
        (5, 'Sports & Outdoors'),
        (6, 'Beauty & Personal Care'),
        (7, 'Toys & Games'),
        (8, 'Health & Wellness')
    ]

    try:
        connection = create_connection()
        cursor = connection.cursor()

        for cat_id, category_name in required_categories:
            # Check if category exists
            query = "SELECT * FROM Categories WHERE cat_id = %s"
            cursor.execute(query, (cat_id,))
            existing_category = cursor.fetchone()

            if not existing_category:
                # Insert category if it doesn't exist
                insert_query = "INSERT INTO Categories (cat_id, category_name) VALUES (%s, %s)"
                cursor.execute(insert_query, (cat_id, category_name))
                print(f"Category '{category_name}' added to Categories table.")

        connection.commit()
        cursor.close()
        connection.close()

        print("All necessary categories added successfully.")

    except Exception as e:
        print("Error adding categories:", e)


def generate_random_email(username):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    domain = random.choice(domains)
    return f'{username}@{domain}'


def create_sellers():
    sellers = [
        {'username': 'Sasi', 'password': 'sasi123',
            'email': generate_random_email('sasi'), 'location': 'Muvattupuzha'},
        {'username': 'Soman', 'password': 'soman123',
            'email': generate_random_email('soman'), 'location': 'Thodupuzha'},
        {'username': 'Ravi', 'password': 'ravi123',
            'email': generate_random_email('ravi'), 'location': 'Vazhakulam'},
        {'username': 'Pushpa', 'password': 'pushpa123',
            'email': generate_random_email('pushpa'), 'location': 'Muvattupuzha'},
        {'username': 'Rangan', 'password': 'rangan123',
            'email': generate_random_email('rangan'), 'location': 'Thodupuzha'},
        {'username': 'Shami', 'password': 'shami123',
            'email': generate_random_email('shami'), 'location': 'Vazhakulam'}
    ]

    connection = create_connection()
    cursor = connection.cursor()

    for seller in sellers:
        username = seller['username']
        password = seller['password']
        email = seller['email']
        location = seller['location']

        # Check if seller already exists
        select_query = "SELECT * FROM Sellers WHERE username = %s"
        cursor.execute(select_query, (username,))
        if cursor.fetchone() is None:
            # Insert seller into Sellers table
            insert_seller_query = """
                INSERT INTO Sellers (username, password, location, email_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_seller_query,
                           (username, password, location, email))
        print(f"Seller : {seller['username']} -> created")

    connection.commit()
    cursor.close()
    connection.close()


def create_users():
    users = [
        {'username': 'Sachin', 'password': 'sachin123',
            'email': generate_random_email('rahul')},
        {'username': 'Renu', 'password': 'renu456',
            'email': generate_random_email('priya')}
    ]

    connection = create_connection()
    cursor = connection.cursor()

    for user in users:
        username = user['username']
        password = user['password']
        email = user['email']

        # Check if user already exists
        select_query = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(select_query, (username,))
        if cursor.fetchone() is None:
            # Insert user into Users table
            insert_user_query = """
                INSERT INTO Users (username, password, email_id)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_user_query, (username, password, email))
        print(f"User : {user['username']} -> created")
    connection.commit()
    cursor.close()
    connection.close()

def insert_product_details():
    # Establish database connection
    try:
        connection = create_connection()
        cursor = connection.cursor()
        # Iterate through each product in the provided details
        for product in products_details:
            # Check if the product already exists in the Products table
            query = "SELECT product_id FROM Products WHERE product_name = %s"
            cursor.execute(query, (product['product_name'],))
            existing_product = cursor.fetchone()

            if existing_product:
                print(f"Product '{product['product_name']}' already exists. Skipping...")
                continue

            # Insert into Products table
            insert_product_query = """
                INSERT INTO Products (product_name, price, description, seller_username, category_id, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_product_query, (
                product['product_name'],
                product['price'],
                product['description'],
                product['seller_username'],
                product['category_id'],
                product['stock']
            ))
            product_id = cursor.lastrowid

            # Insert product images into ProductImages table
            for image_url in product['image_urls']:
                insert_image_query = """
                    INSERT INTO ProductImages (product_id, image_url)
                    VALUES (%s, %s)
                """
                cursor.execute(insert_image_query, (product_id, image_url))

            # Insert review into Reviews table
            insert_review_query = """
                INSERT INTO Reviews (product_id, username, rating, comment)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_review_query, (
                product_id,
                product['review']['username'],
                product['review']['rating'],
                product['review']['comment']
            ))

            print(f"Product '{product['product_name']}' added successfully.")

        # Commit changes to the database
        connection.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

products_details = [
    {
        'product_name': 'Product A',
        'price': 99.99,
        'description': 'High-quality product',
        'seller_username': 'sasi',
        'category_id': 1,
        'stock': 20,
        'image_urls': ['/Backend/images/product-1.jpg', '/Backend/images/galley-3.jpg'],
        'review': {
            'username': 'Sachin',
            'rating': 4,
            'comment': 'Great product!'
        }
    },
    {
        'product_name': 'Product B',
        'price': 49.99,
        'description': 'Affordable option',
        'seller_username': 'soman',
        'category_id': 2,
        'stock': 15,
        'image_urls': ['/Backend/images/product-2.jpg'],
        'review': {
            'username': 'Renu',
            'rating': 5,
            'comment': 'Excellent!'
        }
    }
    # Add more products as needed
]
