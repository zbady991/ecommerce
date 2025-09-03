import pytest
from app import app
from models import db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(
                username='testuser',
                email='test@example.com'
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()  # Ensure session cleanup
            db.drop_all()

def test_login_success(client):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert b'Login successful' in response.data

def test_login_failure(client):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert b'Invalid username or password' in response.data

def test_registration(client):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpass123',
        'confirm_password': 'newpass123'
    }, follow_redirects=True)
    assert b'Registration successful' in response.data
    assert b'Login' in response.data