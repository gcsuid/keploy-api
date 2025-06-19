# keploy-api-assignment

# Simple CRUD API with Python, Flask, and SQLite

This project is a simple yet complete REST API server built using Python. It provides all the basic Create, Read, Update, and Delete (CRUD) operations for a collection of "products".

This server was built to demonstrate the fundamental concepts of how APIs work, from handling HTTP requests to interacting with a database.

## Technology Stack

* **Backend Language**: Python 3
* **Web Framework**: Flask
* **Database**: SQLite 3 (via Python's built-in `sqlite3` module)

## Features

* Create a new product.
* Read a list of all products.
* Read the details of a single product by its ID.
* Update an existing product.
* Delete a product.

## API Endpoints

The base URL for the API is `http://127.0.0.1:5000`.

| Method   | Endpoint           | Description                                    |
| :------- | :----------------- | :--------------------------------------------- |
| `POST`   | `/products`        | Creates a new product.                         |
| `GET`    | `/products`        | Retrieves a list of all products.              |
| `GET`    | `/products/<id>`   | Retrieves a single product by its unique ID.   |
| `PUT`    | `/products/<id>`   | Updates an existing product by its ID.         |
| `DELETE` | `/products/<id>`   | Deletes a product by its ID.                   |

---

## How to Run the Server Locally

To get this project running on your own machine, follow these steps.

**Prerequisites:**
* Python 3 and `pip` installed on your system.
* `git` installed for cloning the repository.

**Step 1: Clone the Repository**
```bash
git clone [https://github.com/your-username/my-python-api.git](https://github.com/your-username/my-python-api.git)
cd my-python-api
```
*(Replace `your-username` with your actual GitHub username.)*

**Step 2: Set Up and Activate a Virtual Environment**
It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it on macOS/Linux
source venv/bin/activate

# Activate it on Windows PowerShell
.\venv\Scripts\activate
```
Your terminal prompt should now start with `(venv)`.

**Step 3: Install Dependencies**
The required Python packages are listed in `requirements.txt`. Install them with `pip`.
```bash
pip install -r requirements.txt
```

**Step 4: Initialize the Database**
This project uses SQLite. Run the `database.py` script once to create the `database.db` file and set up the `products` table.
```bash
python database.py
```

**Step 5: Start the Flask Server**
You are now ready to run the API server.
```bash
flask run
```
The server will start, and you will see output indicating it is running on `http://127.0.0.1:5000`.

---

## How to Test the API

You can use any API client like [Postman](https://www.postman.com/) or a command-line tool like `curl` to interact with the endpoints.

### Using cURL

Here are some example `curl` commands.

* **Create a new product:**

    *(Note for Windows PowerShell users: use `curl.exe` or the `Invoke-WebRequest` examples below)*
    ```bash
    curl -X POST [http://127.0.0.1:5000/products](http://127.0.0.1:5000/products) \
    -H "Content-Type: application/json" \
    -d '{"name": "Wireless Mouse", "description": "Ergonomic and reliable", "price": 25.99}'
    ```

* **Get all products:**
    ```bash
    curl [http://127.0.0.1:5000/products](http://127.0.0.1:5000/products)
    ```

* **Get product with ID 1:**
    ```bash
    curl [http://127.0.0.1:5000/products/1](http://127.0.0.1:5000/products/1)
    ```

### Using Windows PowerShell

If you are using PowerShell, `curl` is an alias for `Invoke-WebRequest`. Use one of the following formats.

* **Create a new product (with `Invoke-WebRequest`):**
    ```powershell
    Invoke-WebRequest -Uri [http://127.0.0.1:5000/products](http://127.0.0.1:5000/products) -Method POST -ContentType "application/json" -Body '{"name": "Wireless Mouse", "description": "Ergonomic and reliable", "price": 25.99}'
    ```

* **Get all products:**
    ```powershell
    Invoke-WebRequest -Uri [http://127.0.0.1:5000/products](http://127.0.0.1:5000/products)
    ```

This README provides a complete guide for anyone (including your future self) to understand, run, and use your project.