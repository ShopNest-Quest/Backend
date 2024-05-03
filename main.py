from flask import Flask, request, jsonify, make_response
from database import check_user_exists, register_user

app = Flask(__name__)

@app.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    if check_user_exists("Admin", username):
        return make_response(jsonify({"message": "User already exists - login to continue"}), 400)

    if register_user("Admin", username, password, email):
        return make_response(jsonify({"message": "Admin registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register admin,Email id already in use"}), 500)

@app.route('/register/user', methods=['POST'])
def register_user_endpoint():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    if check_user_exists("Users", username):
        return make_response(jsonify({"message": "User already exists - login to continue"}), 400)

    if register_user("Users", username, password, email):
        return make_response(jsonify({"message": "User registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register user, Email id already in use"}), 500)

@app.route('/register/seller', methods=['POST'])
def register_seller():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    location = data.get('location')

    if check_user_exists("Sellers", username):
        return make_response(jsonify({"message": "Seller already exists - login to continue"}), 400)

    if register_user("Sellers", username, password, email, location):
        return make_response(jsonify({"message": "Seller registered successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Failed to register seller,Email id already in use"}), 500)

if __name__ == '__main__':
    app.run(debug=True)
