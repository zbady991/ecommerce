from app import app
from models import User

def check_admin():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"Admin user exists:")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Role: {admin.role}")
        else:
            print("Admin user does not exist!")

if __name__ == '__main__':
    check_admin() 