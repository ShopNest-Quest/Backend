from flask import Flask, request, jsonify, make_response
from db_functions import add_product_to_db, authenticate, check_user_exists, get_products_with_ratings_and_images, register
from setup_db import add_default_categories, create_sellers, create_tables, create_users, insert_product_details

app = Flask(__name__)

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


if __name__ == '__main__':
    create_tables()
    add_default_categories()
    create_users()
    create_sellers()
    insert_product_details()
    app.run(debug=True)
