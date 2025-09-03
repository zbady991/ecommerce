from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User, Product
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    # Get featured products (latest 4 products)
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(4).all()
    
    # Define categories
    categories = [
        {
            'name': 'Electronics',
            'icon': 'laptop',
            'description': 'Latest gadgets and electronics'
        },
        {
            'name': 'Fashion',
            'icon': 'bag',
            'description': 'Trendy clothing and accessories'
        },
        {
            'name': 'Home & Living',
            'icon': 'house',
            'description': 'Everything for your home'
        }
    ]
    
    return render_template('index.html', 
                         featured_products=featured_products,
                         categories=categories)

def register_blueprints(app):
    # Import blueprints
    import auth
    import products
    import orders
    import admin

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(admin.bp)

def init_app():
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    register_blueprints(app)
    
    return app

if __name__ == '__main__':
    app = init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
