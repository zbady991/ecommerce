from app import app, db
from models import User

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin account already exists!")
            return

        # Create new admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin123')  # Default password, change this immediately after first login
        
        # Add to database
        db.session.add(admin)
        db.session.commit()
        print("Admin account created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Please change the password after your first login.")

if __name__ == '__main__':
    create_admin() 