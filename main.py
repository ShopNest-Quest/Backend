from flask import Flask, request, jsonify, make_response
from db_functions import add_product_to_db, add_review_to_database, authenticate, change_order_status, change_seller_blocked_status, change_user_blocked_status, check_user_exists, get_order_details_by_username, get_orders_sold_by_seller, get_products_sold_by_seller, get_products_with_ratings_and_images, get_reviews_by_product_id, get_users_or_sellers_with_blocked_status, insert_order, register, update_product_stock
from setup_db import add_default_categories, create_sellers, create_tables, create_users, insert_product_details
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

@app.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    if check_user_exists("Admin", username):
        return make_response(jsonify({"message": "User already exists - login to continue"}), 400)

    if register("Admin", username, password, email):
        return make_response(jsonify({"message": "Admin registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register admin,Email id already in use"}), 412)

@app.route('/register/user', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    if check_user_exists("Users", username):
        return make_response(jsonify({"message": "User already exists - login to continue"}), 400)

    if register("Users", username, password, email):
        return make_response(jsonify({"message": "User registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register user, Email id already in use"}), 412)

@app.route('/register/seller', methods=['POST'])
def register_seller():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    location = data.get('location')

    if check_user_exists("Sellers", username):
        return make_response(jsonify({"message": "Seller already exists - login to continue"}), 400)

    if register("Sellers", username, password, email, location):
        return make_response(jsonify({"message": "Seller registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register seller,Email id already in use"}), 412)

@app.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not check_user_exists("Admin", username):
        return make_response(jsonify({"message": "Admin not found"}), 412)
    if authenticate("Admin", username, password):
        return make_response(jsonify({"message": "Admin login successful"}), 200)
    else:
        return make_response(jsonify({"message": "Invalid credentials"}), 401)

@app.route('/login/user', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

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

@app.route('/login/seller', methods=['POST'])
def login_seller():
    data = request.get_json()
    username = data['username']
    password = data['password']

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

@app.route('/seller/add_product', methods=['POST'])
def add_product():
    product_data = request.get_json()

    result = add_product_to_db(product_data)

    if result["success"]:
        return make_response(jsonify(result), 201)
    else:
        return make_response(jsonify(result), 500)

@app.route('/products', methods=['GET'])
def get_all_products_endpoint():
    try:
        products = get_products_with_ratings_and_images()
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

if __name__ == '__main__':
    create_tables()
    add_default_categories()
    create_users()
    create_sellers()
    insert_product_details()
    app.run(debug=True)
