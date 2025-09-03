from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Product, Order, User

bp = Blueprint('admin', __name__)

@bp.before_request
@login_required
def require_admin():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('index'))

@bp.route('/admin')
def admin_dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    return render_template('admin.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders)

@bp.route('/admin/products')
def manage_products():
    products = Product.query.all()
    return render_template('admin_products.html', products=products)

@bp.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category = request.form['category']
        image_url = request.form['image_url'] or None
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin.manage_products'))
    
    return render_template('add_product.html')

@bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category = request.form['category']
        product.image_url = request.form['image_url'] or None
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.manage_products'))
    
    return render_template('edit_product.html', product=product)

@bp.route('/admin/products/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'info')
    return redirect(url_for('admin.manage_products'))

@bp.route('/admin/orders')
def manage_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_orders.html', orders=orders)

@bp.route('/admin/order/<int:order_id>')
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin_order_detail.html', order=order)

@bp.route('/admin/order/update-status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form['status']
    order.status = new_status
    db.session.commit()
    flash('Order status updated', 'success')
    return redirect(url_for('admin.view_order', order_id=order_id))