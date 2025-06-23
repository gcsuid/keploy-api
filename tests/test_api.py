import pytest
import json
from app import app, get_db_connection

# This is a pytest fixture. It's a special function that sets up
# a resource for our tests to use. Here, we set up a test client.
@pytest.fixture
def client():
    # Use the application's test client
    with app.test_client() as client:
        # Before each test, we'll set up a clean database
        with app.app_context():
            db = get_db_connection()
            # You might want to clear the database and re-initialize it here
            # For simplicity, we assume the database is clean or tests handle state
        yield client # This is where the test runs

# Test for the GET /products endpoint
def test_get_all_products(client):
    """Test retrieving all products."""
    # First, let's add a product to make sure there's something to retrieve
    client.post('/products', data=json.dumps(dict(
        name='Test Product',
        description='A product for testing',
        price=10.0
    )), content_type='application/json')

    # Now, make the GET request
    response = client.get('/products')
    
    # Assert that the request was successful
    assert response.status_code == 200
    # Assert that the response data is a list
    assert isinstance(response.get_json(), list)
    # Assert that our new product is in the list
    assert b'Test Product' in response.data

# Test for the POST /products endpoint
def test_create_product(client):
    """Test creating a new product."""
    response = client.post('/products', data=json.dumps(dict(
        name='New Gadget',
        description='A cool new gadget',
        price=99.99
    )), content_type='application/json')
    
    data = response.get_json()
    
    # Assert the status code is 201 (Created)
    assert response.status_code == 201
    # Assert the response contains the correct product name
    assert 'New Gadget' in data['name']
    # Assert the response contains an ID for the new product
    assert 'id' in data

# Test for getting a single product
def test_get_one_product(client):
    """Test retrieving a single product by its ID."""
    # First create a product to fetch
    post_res = client.post('/products', data=json.dumps(dict(
        name='Specific Product',
        description='Details about this product',
        price=50.0
    )), content_type='application/json')
    
    product_id = post_res.get_json()['id']
    
    # Now get the product by its ID
    get_res = client.get(f'/products/{product_id}')
    
    assert get_res.status_code == 200
    assert get_res.get_json()['name'] == 'Specific Product'

# Test for updating a product
def test_update_product(client):
    """Test updating an existing product."""
    # First create a product to update
    post_res = client.post('/products', data=json.dumps(dict(
        name='Original Name',
        description='Original Description',
        price=10.0
    )), content_type='application/json')
    
    product_id = post_res.get_json()['id']
    
    # Now update the product
    put_res = client.put(f'/products/{product_id}', data=json.dumps(dict(
        name='Updated Name',
        description='Updated Description',
        price=15.0,
        in_stock=False
    )), content_type='application/json')
    
    assert put_res.status_code == 200
    assert b'Product updated successfully' in put_res.data

    # Verify the update by fetching the product again
    get_res = client.get(f'/products/{product_id}')
    assert get_res.get_json()['name'] == 'Updated Name'
    assert get_res.get_json()['price'] == 15.0

# Test for deleting a product
def test_delete_product(client):
    """Test deleting a product."""
    # First create a product to delete
    post_res = client.post('/products', data=json.dumps(dict(
        name='To Be Deleted',
        description='This will be deleted',
        price=1.0
    )), content_type='application/json')
    
    product_id = post_res.get_json()['id']
    
    # Delete the product
    delete_res = client.delete(f'/products/{product_id}')
    assert delete_res.status_code == 200
    
    # Verify it's gone by trying to fetch it again
    get_res = client.get(f'/products/{product_id}')
    assert get_res.status_code == 404