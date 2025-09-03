from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Order, OrderItem, CartItem, Product
from datetime import datetime

bp = Blueprint('orders', __name__)

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('products.cart'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Validate stock
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if item.quantity > product.stock:
                flash(f'Not enough stock for {product.name}', 'error')
                return redirect(url_for('orders.checkout'))
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=request.form['address'],
            payment_method=request.form['payment']
        )
        db.session.add(order)
        db.session.commit()
        
        # Create order items and update stock
        for item in cart_items:
            product = Product.query.get(item.product_id)
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            product.stock -= item.quantity
            
            # Remove from cart
            db.session.delete(item)
        
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('orders.order_confirmation', order_id=order.id))
    
    return render_template('checkout.html', total=total)

@bp.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You cannot view this order', 'error')
        return redirect(url_for('index'))
    
    return render_template('order_confirmation.html', order=order)

@bp.route('/orders')
@login_required
def user_orders():
    if current_user.role == 'admin':
        return redirect(url_for('orders.admin_orders'))
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@bp.route('/admin/orders')
@login_required
def admin_orders():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get filter parameters
    status = request.args.get('status', '')
    date = request.args.get('date', '')
    
    # Base query
    query = Order.query
    
    # Apply filters
    if status:
        query = query.filter(Order.status == status)
    if date:
        try:
            filter_date = datetime.strptime(date, '%Y-%m-%d')
            query = query.filter(db.func.date(Order.created_at) == filter_date.date())
        except ValueError:
            pass
    
    # Get orders with sorting
    orders = query.order_by(Order.created_at.desc()).all()
    
    return render_template('admin/orders.html', orders=orders)

@bp.route('/admin/orders/<int:order_id>')
@login_required
def admin_order_detail(order_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@bp.route('/admin/orders/<int:order_id>/update', methods=['POST'])
@login_required
def update_order_status(order_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}', 'success')
    
    return redirect(url_for('orders.admin_order_detail', order_id=order_id)) 
