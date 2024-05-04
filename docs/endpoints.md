# API Endpoints Documentation

## Register Admin

- **Endpoint**: `/register/admin`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username for admin registration.
- `password` (string): Password for admin registration.
- `email` (string): Email address for admin registration.

### Response

- `201 Created`: Admin registered successfully.
- `400 Bad Request`: User already exists. Prompt to login.
- `412 Precondition Failed`: Failed to register admin. Email ID already in use.

---

## Register User

- **Endpoint**: `/register/user`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username for user registration.
- `password` (string): Password for user registration.
- `email` (string): Email address for user registration.

### Response

- `201 Created`: User registered successfully.
- `400 Bad Request`: User already exists. Prompt to login.
- `412 Precondition Failed`: Failed to register user. Email ID already in use.

---

## Register Seller

- **Endpoint**: `/register/seller`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username for seller registration.
- `password` (string): Password for seller registration.
- `email` (string): Email address for seller registration.
- `location` (string, optional): Location of the seller.

### Response

- `201 Created`: Seller registered successfully.
- `400 Bad Request`: Seller already exists. Prompt to login.
- `412 Precondition Failed`: Failed to register seller. Email ID already in use.

---

## Login Admin

- **Endpoint**: `/login/admin`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username for admin login.
- `password` (string): Password for admin login.

### Response

- `200 OK`: Admin login successful.
- `401 Unauthorized`: Invalid credentials.
- `412 Precondition Failed`: Admin not found.

---

## Login User

- **Endpoint**: `/login/user`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username for user login.
- `password` (string): Password for user login.

### Response

- `200 OK`: User login successful.
- `401 Unauthorized`: Invalid credentials.
- `403 Forbidden`: User account is blocked.
- `412 Precondition Failed`: User not found.

---

## Login Seller

- **Endpoint**: `/login/seller`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username for seller login.
- `password` (string): Password for seller login.

### Response

- `200 OK`: Seller login successful.
- `401 Unauthorized`: Invalid credentials.
- `403 Forbidden`: Seller account is blocked.
- `412 Precondition Failed`: Seller not found.

## Add Product

- **Endpoint**: `/seller/add_product`
- **Method**: `POST`
  
### Parameters

- `product_name` (string): Name of the product.
- `price` (float): Price of the product.
- `description` (string): Description of the product.
- `seller_username` (string): Username of the seller adding the product.
- `category_id` (integer, optional): ID of the category to which the product belongs.
- `stock` (integer, optional): Quantity of the product in stock (default: 0).
- `images` (list of strings, optional): List of URLs of images for the product.

### Response

- `201 Created`: Product added successfully.
  - Body:
    ```json
    {
        "success": true,
        "message": "Product and images added successfully",
        "product_id": <product_id>
    }
    ```
- `500 Internal Server Error`: Failed to add product.
  - Body:
    ```json
    {
        "success": false,
        "message": "Failed to add product"
    }
    ```

---