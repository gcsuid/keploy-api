import pytest
from unittest.mock import patch, MagicMock
from app import create_product  # We are importing a specific function now
from flask import Flask

# Unit Test for the create_product function using mocking
@patch('app.get_db_connection')  # This line is the key to mocking
def test_create_product_unit(mock_get_db_connection):
    """
    This test checks the create_product function's logic
    without using a real database.
    """
    # 1. Setup the Mock
    # We create a fake database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # When the function asks for a cursor, give it our fake one
    mock_conn.cursor.return_value = mock_cursor
    # When the code calls get_db_connection(), it will get our fake connection
    mock_get_db_connection.return_value = mock_conn
    
    # Let's pretend the database gives us '5' as the new ID
    mock_cursor.lastrowid = 5

    # 2. Call the function inside a Flask app context
    # Our function needs a 'request' object, which only exists inside a real request
    # We create a minimal Flask app to simulate this context
    app = Flask(__name__)
    with app.test_request_context(json={
        "name": "Mock Product",
        "description": "A product created with a mock DB",
        "price": 123.45
    }):
        # Run the function we are testing
        response, status_code = create_product()

    # 3. Assert the results
    # Check that our function tried to execute the correct SQL
    mock_cursor.execute.assert_called_with(
        'INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
        ('Mock Product', 'A product created with a mock DB', 123.45)
    )
    # Check that our function tried to save the changes
    mock_conn.commit.assert_called_once()
    # Check that the status code is correct
    assert status_code == 201
    # Check that the response JSON contains the mock ID
    assert response.get_json()['id'] == 5