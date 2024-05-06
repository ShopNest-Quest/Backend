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

## Get All Products

- **Endpoint**: `/products`
- **Method**: `GET`
  
### Description

This endpoint retrieves all products along with their details, including ratings and images.

### Response

- `200 OK`: Products retrieved successfully.
  - Body:
    ```json
    {
        "products": [
            {
                "average_rating": null,
                "description": "This is a \"sample\" product with special characters",
                "images": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg"
                ],
                "price": 19.99,
                "product_id": 1,
                "product_name": "Sample Product",
                "seller_username": "seller123"
            },
            {
                "average_rating": 3.5,
                "description": "This is a sample product.",
                "images": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg"
                ],
                "price": 29.99,
                "product_id": 2,
                "product_name": "Sample Product 2",
                "seller_username": "seller1234"
            }
        ]
    }
    ```
- `500 Internal Server Error`: Failed to retrieve products.
  - Body:
    ```json
    {
        "error": "<error_message>"
    }
    ```

---

## Place Order

- **Endpoint**: `/place_order`
- **Method**: `POST`
  
### Parameters

- `customer_username` (string): Username of the customer placing the order.
- `product_id` (integer): ID of the product being ordered.
- `quantity` (integer): Quantity of the product being ordered.

### Response

- `200 OK`: Order placed successfully.
  - Body:
    ```json
    {
        "message": "Order added successfully",
        "total_price": <total_price>
    }
    ```
- `500 Internal Server Error`: Failed to place the order.
  - Body:
    ```json
    {
        "message": "<error_message>"
    }
    ```

---
## Get User Orders

- **Endpoint**: `/get_user_orders`
- **Method**: `GET`
  
### Parameters

- `customer_username` (string): Username of the customer whose orders are to be retrieved.

### Response

- `200 OK`: Orders retrieved successfully.
  - Body:
    ```json
    {
        "orders": [
            {
                "order_date": "<order_date>",
                "product_name": "<product_name>",
                "price": <price>,
                "quantity": <quantity>,
                "total_price": <total_price>,
                "status": "<status>",
                "image_url": "<image_url>"
            },
            {
                "order_date": "<order_date>",
                "product_name": "<product_name>",
                "price": <price>,
                "quantity": <quantity>,
                "total_price": <total_price>,
                "status": "<status>",
                "image_url": "<image_url>"
            },
            ...
        ]
    }
    ```
- `500 Internal Server Error`: Failed to retrieve orders.
  - Body:
    ```json
    {
        "message": "<error_message>"
    }
    ```

---
## Get Seller Orders

- **Endpoint**: `/get_seller_orders`
- **Method**: `GET`
  
### Parameters

- `seller_username` (string): Username of the seller whose orders are to be retrieved.

### Response

- `200 OK`: Orders retrieved successfully.
  - Body:
    ```json
    {
        "message": [
            {
                "order_date": "<formatted_order_date>",
                "product_name": "<product_name>",
                "price": <price>,
                "quantity": <quantity>,
                "total_price": <total_price>,
                "status": "<status>",
                "image_url": "<image_url>",
                "product_id": <product_id>,
                "order_id" : <order_id>
            },
            {
                "order_date": "<formatted_order_date>",
                "product_name": "<product_name>",
                "price": <price>,
                "quantity": <quantity>,
                "total_price": <total_price>,
                "status": "<status>",
                "image_url": "<image_url>",
                "product_id": <product_id>,
                "order_id" : <order_id>
            },
            ...
        ]
    }
    ```
- `500 Internal Server Error`: Failed to retrieve orders.
  - Body:
    ```json
    {
        "message": "<error_message>"
    }
    ```

---
## Get Product Reviews

- **Endpoint**: `/product_reviews`
- **Method**: `GET`
  
### Parameters

- `product_id` (integer): ID of the product whose reviews are to be retrieved.

### Response

- `200 OK`: Reviews retrieved successfully.
  - Body:
    ```json
    {
        "reviews": [
            {
                "review_id": <review_id>,
                "username": "<username>",
                "rating": <rating>,
                "comment": "<comment>",
                "review_date": "<formatted_review_date>"
            },
            {
                "review_id": <review_id>,
                "username": "<username>",
                "rating": <rating>,
                "comment": "<comment>",
                "review_date": "<formatted_review_date>"
            },
            ...
        ]
    }
    ```
- `404 Not Found`: No reviews found for the specified product.
  - Body:
    ```json
    {
        "message": "No reviews found for this product"
    }
    ```

---
## Update Order Status

- **Endpoint**: `/update_order_status`
- **Method**: `POST`
  
### Parameters

- `order_id` (integer): ID of the order to be updated.
- `new_status` (string): New status to set for the order. Allowed values: `'pending'`, `'shipped'`, `'delivered'`.

### Response

- `200 OK`: Order status updated successfully.
  - Body:
    ```json
    {
        "message": "Order status updated to <new_status>"
    }
    ```
- `404 Not Found`: Order not found with the specified `order_id`.
  - Body:
    ```json
    {
        "message": "Order with order_id <order_id> not found"
    }
    ```

---
## Get Seller Products

- **Endpoint**: `/get_seller_products`
- **Method**: `GET`
  
### Parameters

- `seller_username` (string): Username of the seller whose products are to be retrieved.

### Response

- `200 OK`: Products retrieved successfully.
  - Body:
    ```json
    {
        "products": [
            {
                "product_id": <product_id>,
                "product_name": "<product_name>",
                "price": <price>,
                "description": "<description>",
                "seller_username": "<seller_username>",
                "average_rating": <average_rating>,
                "images": ["<image_url1>", "<image_url2>", ...],
                "stock": <stock>
            },
            {
                "product_id": <product_id>,
                "product_name": "<product_name>",
                "price": <price>,
                "description": "<description>",
                "seller_username": "<seller_username>",
                "average_rating": <average_rating>,
                "images": ["<image_url1>", "<image_url2>", ...],
                "stock": <stock>
            },
            ...
        ]
    }
    ```
- `500 Internal Server Error`: Failed to retrieve products.
  - Body:
    ```json
    {
        "message": "<error_message>"
    }
    ```

---
## Update Product Stock

- **Endpoint**: `/update_product_stock`
- **Method**: `POST`
  
### Parameters

- `product_id` (integer): ID of the product to update.
- `new_stock` (integer): New stock quantity for the product.

### Response

- `200 OK`: Product stock updated successfully.
  - Body:
    ```json
    {
        "message": "Product stock updated to <new_stock>"
    }
    ```
- `404 Not Found`: Product not found with the specified `product_id`.
  - Body:
    ```json
    {
        "message": "Product with product_id <product_id> not found"
    }
    ```

---
## Change User Blocked Status

- **Endpoint**: `/change_user_status`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username of the user whose blocked status is to be updated.
- `isblocked` (int): New blocked status for the user (`1` to block, `0` to unblock).

### Response

- `200 OK`: User blocked status updated successfully.
  - Body:
    ```json
    {
        "message": "User '<username>' blocked status updated successfully"
    }
    ```
- `404 Not Found`: User not found with the specified `username`.
  - Body:
    ```json
    {
        "message": "User with username '<username>' not found"
    }
    ```

---
## Change Seller Blocked Status

- **Endpoint**: `/change_seller_status`
- **Method**: `POST`
  
### Parameters

- `username` (string): Username of the user whose blocked status is to be updated.
- `isblocked` (int): New blocked status for the user (`1` to block, `0` to unblock).

### Response

- `200 OK`: User blocked status updated successfully.
  - Body:
    ```json
    {
        "message": "Seller '<username>' blocked status updated successfully"
    }
    ```
- `404 Not Found`: User not found with the specified `username`.
  - Body:
    ```json
    {
        "message": "Seller with username '<username>' not found"
    }
    ```

---
## `/get_users`

- **Endpoint**: `/get_users`
- **Method**: `GET`
  
### Response

- `200 OK`: Users retrieved successfully.
  - Body:
    ```json
    {
        "users": [
            {
                "username": "<username>",
                "isBlocked": <is_blocked>
            },
            {
                "username": "<username>",
                "isBlocked": <is_blocked>
            },
            ...
        ]
    }
    ```
- `500 Internal Server Error`: Failed to retrieve users.
  - Body:
    ```json
    {
        "error": "Failed to retrieve users"
    }
    ```

---

## `/get_sellers`

- **Endpoint**: `/get_sellers`
- **Method**: `GET`
  
### Response

- `200 OK`: Sellers retrieved successfully.
  - Body:
    ```json
    {
        "sellers": [
            {
                "username": "<username>",
                "isBlocked": <is_blocked>
            },
            {
                "username": "<username>",
                "isBlocked": <is_blocked>
            },
            ...
        ]
    }
    ```
- `500 Internal Server Error`: Failed to retrieve sellers.
  - Body:
    ```json
    {
        "error": "Failed to retrieve sellers"
    }
    ```

---
# Add Review

- **Endpoint**: `/add_review`
- **Method**: `POST`
  
### Request Body

- `product_id` (integer): ID of the product being reviewed.
- `username` (string): Username of the reviewer.
- `rating` (integer): Rating given for the product (1-5).
- `comment` (string, optional): Review comment.

### Response

- `201 Created`: Review added successfully.
  - Body:
    ```json
    {
        "message": "Review added successfully"
    }
    ```
- `400 Bad Request`: Missing required fields in the request body.
  - Body:
    ```json
    {
        "error": "Missing required fields"
    }
    ```
- `500 Internal Server Error`: Failed to add the review due to a server error.
  - Body:
    ```json
    {
        "error": "An unexpected error occurred: <error_message>"
    }
    ```

---