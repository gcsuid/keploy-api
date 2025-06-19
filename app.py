import sqlite3
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# A helper function to get a database connection.
# This makes connecting and setting the row factory for dictionary-like row access easier.
def get_db_connection():
    # Connect to the SQLite database file specified
    conn = sqlite3.connect('database.db')
    # This line allows you to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

# --- API Endpoints ---

# Endpoint 1: CREATE a new product
# URL: /products
# Method: POST
@app.route('/products', methods=['POST'])
def create_product():
    # Get the JSON data from the request body
    data = request.get_json()
    
    # Extract data from the JSON payload
    name = data['name']
    description = data['description']
    price = data['price']
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute the SQL INSERT statement
    cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
                   (name, description, price))
                   
    # Get the ID of the newly created product
    product_id = cursor.lastrowid
    
    # Commit the transaction to save the changes
    conn.commit()
    # Close the database connection
    conn.close()
    
    # Return the newly created product's data along with its ID
    return jsonify({'id': product_id, **data}), 201

# Endpoint 2: READ all products
# URL: /products
# Method: GET
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    # Execute a SELECT query to fetch all products
    products_cursor = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    # Convert the list of Row objects into a list of dictionaries
    products_list = [dict(product) for product in products_cursor]
    
    # Return the list of products as a JSON response
    return jsonify(products_list)

# Endpoint 3: READ a single product by its ID
# URL: /products/<id>
# Method: GET
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    # Fetch one product by its ID
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    # If no product is found, return a 404 Not Found error
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
        
    # Return the product data as a JSON response
    return jsonify(dict(product))

# Endpoint 4: UPDATE a product by its ID
# URL: /products/<id>
# Method: PUT
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']
    # Use .get() for optional fields with a default value
    in_stock = data.get('in_stock', True)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute the SQL UPDATE statement
    cursor.execute('UPDATE products SET name = ?, description = ?, price = ?, in_stock = ? WHERE id = ?',
                   (name, description, price, in_stock, product_id))
    conn.commit()
    
    # Check if any row was actually updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Product not found'}), 404
            
    conn.close()
    # Return a success message
    return jsonify({'message': 'Product updated successfully'})

# Endpoint 5: DELETE a product by its ID
# URL: /products/<id>
# Method: DELETE
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Execute the SQL DELETE statement
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    
    # Check if any row was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Product not found'}), 404
            
    conn.close()
    # Return a success message
    return jsonify({'message': 'Product deleted successfully'})

# This block allows you to run the app directly from the command line
if __name__ == '__main__':
    # debug=True will auto-reload the server when you make changes
    app.run(debug=True)