# ShopNest Backend Setup Guide

Follow these steps to run the backend server for ShopNest:

1. **Update Database Configuration**
   - Open `config_db.py` located in the backend project directory.
   - Modify the database connection parameters (`host`, `user`, `password`, `database`) according to your MySQL setup. By default:
     ```python
     host = "localhost"
     user = "root"
     password = "root@123"
     database = "shopnest"
     ```

2. **Create MySQL Database**
   - Ensure [MySQL](https://dev.mysql.com/downloads/mysql/) is installed and running.
   - Create a database named `shopnest` (or as configured in `config_db.py`) using your preferred MySQL client.

3. **Set Up Virtual Environment**
   - Create a virtual environment for the project. Use the following commands:
     ```bash
     python3 -m venv env
     ```

4. **Activate the Virtual Environment**
   - Activate the virtual environment based on your operating system:
     - For Unix/Linux:
       ```bash
       source env/bin/activate
       ```
     - For Windows:
       ```bash
       .\env\Scripts\activate
       ```
       or
       
       ```bash
       .\env\bin\activate
       ```

5. **Install Project Requirements**
   - Install the required Python packages listed in `requirements.txt` using pip:
     ```bash
     pip install -r requirements.txt
     ```

6. **Run the Backend Server**
   - Start the Flask server by running `main.py`:
     ```bash
     python3 main.py
     ```

Now the ShopNest backend server should be running locally. You can access it at the specified host and port defined in `main.py`. Make sure all dependencies are installed and the database connection is properly configured before running the server.
