from flask import Flask, request, jsonify, make_response
from config_db import create_connection
from db_functions import add_product_to_db, add_review_to_database, authenticate, change_order_status, change_seller_blocked_status, change_user_blocked_status, check_user_exists, get_order_details_by_username, get_orders_sold_by_seller, get_products_sold_by_seller, get_products_with_ratings_and_images, get_reviews_by_product_id, get_users_or_sellers_with_blocked_status, insert_order, register, update_product_stock
from setup_db import add_default_categories, create_sellers, create_tables, create_users, insert_dummy_user, insert_product_details
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

@app.route('/register/admin', methods=['GET'])
def register_admin():
    username = request.args.get("username")
    password = request.args.get('password')
    email = request.args.get('email')

    if check_user_exists("Admin", username):
        return make_response(jsonify({"message": "User already exists - login to continue"}), 400)

    if register("Admin", username, password, email):
        return make_response(jsonify({"message": "Admin registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register admin,Email id already in use"}), 412)

@app.route('/register/user', methods=['GET'])
def register_user():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    if check_user_exists("Users", username):
        return make_response(jsonify({"message": "User already exists - login to continue"}), 400)

    if register("Users", username, password, email):
        return make_response(jsonify({"message": "User registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register user, Email id already in use"}), 412)

@app.route('/register/seller', methods=['GET'])
def register_seller():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    location = request.args.get('location')

    if check_user_exists("Sellers", username):
        return make_response(jsonify({"message": "Seller already exists - login to continue"}), 400)

    if register("Sellers", username, password, email, location):
        return make_response(jsonify({"message": "Seller registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register seller,Email id already in use"}), 412)

@app.route('/login/admin', methods=['GET'])
def login_admin():
    username = request.args.get('username')
    password = request.args.get('password')

    if not check_user_exists("Admin", username):
        return make_response(jsonify({"message": "Admin not found"}), 412)
    if authenticate("Admin", username, password):
        return make_response(jsonify({"message": "Admin login successful"}), 200)
    else:
        return make_response(jsonify({"message": "Invalid credentials"}), 401)

@app.route('/login/user', methods=['GET'])
def login_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if not check_user_exists("Users", username):
        return make_response(jsonify({"message": "User not found"}), 412)
    user_info = authenticate("Users", username, password)
    if user_info:
        if user_info['isBlocked']:
            return make_response(jsonify({"message": "User account is blocked"}), 403)
        else:
            return make_response(jsonify({"message": "User login successful"}), 200)
    else:
        return make_response(jsonify({"message": "Invalid credentials"}), 401)

@app.route('/login/seller', methods=['GET'])
def login_seller():
    username = request.args.get('username')
    password = request.args.get('password')

    if not check_user_exists("Sellers", username):
        return make_response(jsonify({"message": "Seller not found"}), 412)
    seller_info = authenticate("Sellers", username, password)
    if seller_info:
        if seller_info['isBlocked']:
            return make_response(jsonify({"message": "Seller account is blocked"}), 403)
        else:
            return make_response(jsonify({"message": "Seller login successful"}), 200)
    else:
        return make_response(jsonify({"message": "Invalid credentials"}), 401)

@app.route('/seller/add_product', methods=['GET'])
def add_product():
    # Extract parameters from the URL query string
    product_name = request.args.get('product_name')
    price = request.args.get('price')
    description = request.args.get('description')
    seller_username = request.args.get('seller_username')
    category_id = request.args.get('category_id', None)
    stock = request.args.get('stock', 0)
    image_url = request.args.get('image_url')  # Single image URL as a parameter

    # Validate required parameters
    if not all([product_name, price, description, seller_username, image_url]):
        return make_response(jsonify({"success": False, "message": "Missing required parameters"}), 400)

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Insert product details into Products table
        insert_query = """
            INSERT INTO Products (product_name, price, description, seller_username, category_id, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (product_name, price, description, seller_username, category_id, stock))
        product_id = cursor.lastrowid  # Get the auto-generated product_id

        # Insert product image into ProductImages table
        insert_image_query = """
            INSERT INTO ProductImages (product_id, image_url)
            VALUES (%s, %s)
        """
        cursor.execute(insert_image_query, (product_id, image_url))

        connection.commit()
        cursor.close()
        connection.close()

        return make_response(jsonify({"success": True, "message": "Product and image added successfully", "product_id": product_id}), 201)

    except Exception as e:
        print("Error adding product:", e)
        return make_response(jsonify({"success": False, "message": "Failed to add product"}), 500)

@app.route('/products', methods=['GET'])
def get_all_products_endpoint():
    try:
        location = request.args.get('location')
        products = get_products_with_ratings_and_images(location)
        return jsonify({'products': products}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    customer_username = data['customer_username']
    product_id = data['product_id']
    quantity = data['quantity']

    success, message = insert_order(customer_username, product_id, quantity)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 500

@app.route('/get_user_orders', methods=['GET'])
def get_user_orders():
    customer_username = request.args.get('customer_username')
    success, message = get_order_details_by_username(customer_username)

    if success:
        return jsonify(message), 200
    else:
        return jsonify({"message": message}), 500

@app.route('/get_seller_orders', methods=['GET'])
def get_seller_orders():
    seller_username = request.args.get('seller_username')
    success, message = get_orders_sold_by_seller(seller_username)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 500

@app.route('/product_reviews', methods=['GET'])
def product_reviews():
    product_id = request.args.get('product_id')

    success, result = get_reviews_by_product_id(product_id)

    if success:
        return jsonify({"reviews": result}), 200
    else:
        return jsonify({"message": result}), 404

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    order_id = data['order_id']
    new_status = data['new_status']

    success, message = change_order_status(order_id, new_status)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 404

@app.route('/get_seller_products', methods=['GET'])
def get_seller_products():
    seller_username = request.args.get('seller_username')
    success, message = get_products_sold_by_seller(seller_username)

    if success:
        return jsonify({"products" :message}), 200
    else:
        return jsonify({"message": message}), 500

@app.route('/update_product_stock', methods=['POST'])
def update_product_stock_route():
    data = request.get_json()
    product_id = data['product_id']
    new_stock = data['new_stock']

    success, message = update_product_stock(product_id, new_stock)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 404

@app.route('/change_user_status', methods=['POST'])
def change_user_status():
    data = request.get_json()
    username = data['username']
    status = data['isblocked']

    success, message = change_user_blocked_status(username, status)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 404

@app.route('/change_seller_status', methods=['POST'])
def change_seller_status():
    data = request.get_json()
    username = data['username']
    status = data['isblocked']

    success, message = change_seller_blocked_status(username, status)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 404

@app.route('/get_users', methods=['GET'])
def get_users():
    """Route to retrieve users with their 'isBlocked' status."""
    users_data = get_users_or_sellers_with_blocked_status("users")
    if users_data is not None:
        return jsonify(users=users_data)
    else:
        return jsonify(error="Failed to retrieve users"), 500

@app.route('/get_sellers', methods=['GET'])
def get_sellers():
    """Route to retrieve sellers with their 'isBlocked' status."""
    sellers_data = get_users_or_sellers_with_blocked_status("sellers")
    if sellers_data is not None:
        return jsonify(sellers=sellers_data)
    else:
        return jsonify(error="Failed to retrieve sellers"), 500

@app.route('/add_review', methods=['POST'])
def add_review():
    """Endpoint to add a review to the 'reviews' table."""
    try:
        review_data = request.json
        product_id = review_data.get('product_id')
        username = review_data.get('username')
        rating = review_data.get('rating')
        comment = review_data.get('comment')

        if not all([product_id, username, rating]):
            return jsonify(error="Missing required fields"), 400

        success, message = add_review_to_database(product_id, username, rating, comment)
        if success:
            return jsonify(message=message), 201
        else:
            return jsonify(error=message), 500

    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {e}"), 500

@app.route('/cart/add', methods=['GET'])
def add_to_cart():
    username = request.args.get('username')
    product_id = request.args.get('product_id')
    quantity = int(request.args.get('quantity', 1))  # Default quantity is 1 if not provided

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Retrieve product details (price) to add to cart
        cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
        product_price = cursor.fetchone()[0]

        # Calculate total price
        total_price = product_price * quantity

        # Insert into Cart table
        insert_query = """
            INSERT INTO Cart (customer_username, product_id, quantity, price, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, product_id, quantity, product_price, total_price))

        connection.commit()
        cursor.close()
        connection.close()

        return make_response(jsonify({"success": True, "message": "Product added to cart"}), 200)

    except Exception as e:
        print("Error adding to cart:", e)
        return make_response(jsonify({"success": False, "message": "Failed to add product to cart"}), 500)

@app.route('/cart/remove', methods=['GET'])
def remove_from_cart():
    username = request.args.get('username')

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Delete entry from Cart table
        delete_query = "DELETE FROM Cart WHERE customer_username = %s"
        cursor.execute(delete_query, (username,))

        connection.commit()
        cursor.close()
        connection.close()

        return make_response(jsonify({"success": True, "message": "Product removed from cart"}), 200)

    except Exception as e:
        print("Error removing from cart:", e)
        return make_response(jsonify({"success": False, "message": "Failed to remove product from cart"}), 500)
    
@app.route('/cart/details', methods=['GET'])
def get_cart_details():
    username = request.args.get('username')

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Retrieve cart details for the specified user
        select_query = """
            SELECT c.cart_id, p.product_id, p.product_name, p.price, c.quantity, c.total_price
            FROM Cart c
            JOIN Products p ON c.product_id = p.product_id
            WHERE c.customer_username = %s
        """
        cursor.execute(select_query, (username,))
        cart_details = cursor.fetchall()

        # Prepare response data
        products_in_cart = []
        for cart_item in cart_details:
            cart_id, product_id, product_name, price, quantity, total_price = cart_item
            product_info = {
                "cart_id": cart_id,
                "product_id": product_id,
                "product_name": product_name,
                "price": float(price),  # Convert decimal to float for JSON serialization
                "quantity": quantity,
                "total_price": float(total_price)  # Convert decimal to float for JSON serialization
            }
            products_in_cart.append(product_info)

        cursor.close()
        connection.close()

        return make_response(jsonify({"success": True, "cart": products_in_cart}), 200)

    except Exception as e:
        print("Error fetching cart details:", e)
        return make_response(jsonify({"success": False, "message": "Failed to fetch cart details"}), 500)

if __name__ == '__main__':
    create_tables()
    add_default_categories()
    create_users()
    create_sellers()
    insert_product_details()
    insert_dummy_user('admin','admin123','admin@shopnest.com')
    app.run(debug=True)
