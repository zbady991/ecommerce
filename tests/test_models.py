import pytest
from models import User, Product, CartItem, Order, OrderItem, db
from werkzeug.security import check_password_hash

@pytest.fixture
def new_user():
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashedpassword'
    )
    return user

@pytest.fixture
def new_product():
    product = Product(
        name='Test Product',
        description='Test Description',
        price=9.99,
        stock=10
    )
    return product

def test_new_user(new_user):
    assert new_user.username == 'testuser'
    assert new_user.email == 'test@example.com'
    assert check_password_hash(new_user.password_hash, 'hashedpassword') is True  # Corrected assertion
    assert new_user.role == 'customer'

def test_set_password(new_user):
    new_user.set_password('newpassword')
    assert new_user.check_password('newpassword') is True
    assert new_user.check_password('wrongpassword') is False

def test_new_product(new_product):
    assert new_product.name == 'Test Product'
    assert new_product.price == 9.99
    assert new_product.stock == 10
    assert new_product.category is None

def test_cart_item_relationship(new_user, new_product):
    cart_item = CartItem(
        user=new_user,
        product=new_product,
        quantity=2
    )
    assert cart_item.user.username == 'testuser'
    assert cart_item.product.name == 'Test Product'
    assert cart_item.quantity == 2