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