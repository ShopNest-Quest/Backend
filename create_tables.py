import mysql.connector

# Establishing a connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="shopnest"
)

# Creating a cursor object using the connection
cursor = db_connection.cursor()

# Define SQL statements for table creation in correct order
create_tables = [
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

# Execute each table creation statement
for create_table_query in create_tables:
    try:
        cursor.execute(create_table_query)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# Committing the transaction and closing the connection
db_connection.commit()
cursor.close()
db_connection.close()
