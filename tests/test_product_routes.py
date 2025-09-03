import pytest
from app import app
from models import db, User, Product

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user and product
            user = User(
                username='testuser',
                email='test@example.com'
            )
            user.set_password('testpass')
            product = Product(
                name='Test Product',
                price=9.99,
                stock=10
            )
            db.session.add_all([user, product])
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()  # Ensure session cleanup
            db.drop_all()

def test_product_list(client):
    response = client.get('/products')
    assert b'Test Product' in response.data

def test_add_to_cart(client):
    # Login first
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    response = client.post('/products/add-to-cart/1', data={
        'quantity': '1'
    }, follow_redirects=True)
    assert b'Product added to cart' in response.data
    assert b'Test Product' in response.data