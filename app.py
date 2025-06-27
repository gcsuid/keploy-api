import sqlite3
from flask import Flask, request, jsonify
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# --- 1. App Initialization ---
app = Flask(__name__)

# --- 2. OpenAPI Schema Generation Setup ---
# This part creates the blueprint for our API documentation.
spec = APISpec(
    title='Product API',
    version='1.0.0',
    openapi_version='2.0', # Using OpenAPI 2.0 for broader compatibility
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

# Define Marshmallow Schemas. These describe the shape of our JSON data.
class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    in_stock = fields.Bool()
    created_at = fields.Str(dump_only=True)

# --- 3. Database Helper Function ---
# A reusable function to get a connection to our SQLite database.
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # This line makes the database rows accessible by column name (like a dictionary).
    conn.row_factory = sqlite3.Row
    return conn

# --- 4. API Endpoints ---
# Each function below corresponds to a specific API endpoint.

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product
    ---
    post:
      summary: Creates a new product.
      description: Creates a new product in the database from the provided JSON data.
      requestBody:
          required: true
          content:
            application/json:
              schema: ProductSchema
      responses:
        201:
          description: Product created successfully.
          content:
            application/json:
              schema: ProductSchema
    """
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
                   (name, description, price))
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': product_id, **data}), 201

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products
    ---
    get:
      summary: Retrieve all products.
      description: Returns a list of all products currently in the database.
      responses:
        200:
          description: A list of products.
          content:
            application/json:
              schema:
                type: array
                items: ProductSchema
    """
    conn = get_db_connection()
    products_cursor = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    return jsonify([dict(product) for product in products_cursor])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID
    ---
    get:
        summary: Retrieve a single product.
        parameters:
          - in: path
            name: product_id
            required: true
            schema:
              type: integer
            description: The ID of the product to retrieve.
        responses:
            200:
                description: Product details.
                content:
                    application/json:
                        schema: ProductSchema
            404:
                description: Product not found.
    """
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
        
    return jsonify(dict(product))

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product
    ---
    put:
        summary: Update an existing product.
        parameters:
          - in: path
            name: product_id
            required: true
            schema:
              type: integer
            description: The ID of the product to update.
        requestBody:
          required: true
          content:
            application/json:
              schema: ProductSchema
        responses:
            200:
                description: Product updated successfully.
            404:
                description: Product not found.
    """
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']
    in_stock = data.get('in_stock', True)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET name = ?, description = ?, price = ?, in_stock = ? WHERE id = ?',
                   (name, description, price, in_stock, product_id))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Product not found'}), 404
            
    conn.close()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product
    ---
    delete:
        summary: Delete a product by its ID.
        parameters:
          - in: path
            name: product_id
            required: true
            schema:
              type: integer
            description: The ID of the product to delete.
        responses:
            200:
                description: Product deleted successfully.
            404:
                description: Product not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Product not found'}), 404
            
    conn.close()
    return jsonify({'message': 'Product deleted successfully'})


# --- 5. Register Endpoints with APISpec and Serve the Schema ---

# This block tells APISpec to scan the docstrings of our functions.
with app.app_context():
    spec.path(view=create_product)
    spec.path(view=get_products)
    spec.path(view=get_product)
    spec.path(view=update_product)
    spec.path(view=delete_product)

# Create a new route to serve the generated OpenAPI specification.
@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


# --- 6. Run the Application ---
# This block allows you to run the app directly using "python app.py"
if __name__ == '__main__':
    app.run(debug=True, port=5000)