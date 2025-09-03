from app import app, db
from sqlalchemy import text

def update_database():
    with app.app_context():
        # Drop the banners table if it exists
        with db.engine.connect() as conn:
            conn.execute(text('DROP TABLE IF EXISTS banners'))
            conn.commit()
        
        # Add is_active column to users table if it doesn't exist
        conn.execute(text('ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1'))
        conn.commit()
        
        # Recreate all tables
        db.create_all()

if __name__ == '__main__':
    update_database()
    print("Database updated successfully!") 