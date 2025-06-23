# Simple CRUD API with Python, Flask, and SQLite

This project is a simple yet complete REST API server built using Python. It provides all the basic Create, Read, Update, and Delete (CRUD) operations for a collection of "products".

This project was built to demonstrate the fundamental concepts of how APIs work, from handling HTTP requests to interacting with a database. It also includes a full suite of API, integration, and unit tests to ensure code quality and reliability.

## Technology Stack

* **Backend Language**: Python 3
* **Web Framework**: Flask
* **Database**: SQLite 3 (via Python's built-in `sqlite3` module)
* **Testing Frameworks**: `pytest` for running tests and `pytest-cov` for measuring code coverage.

## Features

* Create, Read, Update, and Delete products via API endpoints.
* Unit and integration tested with high code coverage.
* Demonstrates mocking for database-independent unit tests.

## API Endpoints

The base URL for the API is `http://127.0.0.1:5000`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/products` | Creates a new product. |
| `GET` | `/products` | Retrieves a list of all products. |
| `GET` | `/products/<id>` | Retrieves a single product by its unique ID. |
| `PUT` | `/products/<id>` | Updates an existing product by its ID. |
| `DELETE` | `/products/<id>` | Deletes a product by its ID. |

---

## How to Run the Server Locally

To get this project running on your own machine, follow these steps.

**Prerequisites:**
* Python 3 and `pip` installed on your system.
* `git` installed for cloning the repository.

**1. Clone the Repository**
```bash
git clone [https://github.com/your-username/keploy-api.git](https://github.com/your-username/keploy-api.git)
cd keploy-api
```
*(Replace `your-username` with your actual GitHub username, `gcsuid`)*

**2. Set Up and Activate a Virtual Environment**
Using a virtual environment is highly recommended to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\activate

# Activate on macOS/Linux
# source venv/bin/activate
```
Your terminal prompt should now start with `(venv)`.

**3. Install Dependencies**
The required Python packages are listed in `requirements.txt`. Install them with `pip`.
```bash
pip install -r requirements.txt
```

**4. Initialize the Database**
This script creates the `database.db` file and sets up the `products` table. It only needs to be run once.
```bash
python database.py
```

**5. Start the Flask Server**
You are now ready to run the API server.
```bash
flask run
```
The API will now be running at `http://127.0.0.1:5000`.

---

## Testing the Application

This project uses `pytest` for testing.

**1. How to Run Tests**
To run the entire test suite, make sure your virtual environment is activated and run the following command from the project's root directory:
```bash
# This command works if you have a pytest.ini file
pytest

# This is a more direct way that always works
python -m pytest
```

**2. How to Get a Coverage Report**
To run the tests and generate a code coverage report for the `app.py` file, run:
```bash
python -m pytest --cov=app
```

