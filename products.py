from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Product, CartItem
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('products', __name__)

@bp.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('products.html', products=products)

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash('Not enough stock available', 'error')
        return redirect(url_for('products.product_detail', product_id=product_id))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart', 'success')
    return redirect(url_for('products.cart'))

@bp.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@bp.route('/remove-from-cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('You cannot remove this item', 'error')
        return redirect(url_for('products.cart'))
    
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart', 'info')
    return redirect(url_for('products.cart'))

@bp.route('/admin/products')
@login_required
def admin_products():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@bp.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category = request.form.get('category')
        image = request.files.get('image')
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/product_images', filename))
            image_url = f'/static/product_images/{filename}'
        else:
            image_url = None
        
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
        return redirect(url_for('products.admin_products'))
    
    return render_template('admin/add_product.html')

@bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.category = request.form.get('category')
        
        # Handle discount fields
        product.discount_percent = float(request.form.get('discount_percent', 0))
        
        # Handle discount dates
        start_date = request.form.get('discount_start_date')
        end_date = request.form.get('discount_end_date')
        
        if start_date:
            product.discount_start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        else:
            product.discount_start_date = None
            
        if end_date:
            product.discount_end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        else:
            product.discount_end_date = None
        
        # Handle image upload
        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/product_images', filename))
            product.image_url = f'/static/product_images/{filename}'
        
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('products.admin_products'))
    
    return render_template('admin/edit_product.html', product=product)

@bp.route('/admin/products/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'info')
    return redirect(url_for('products.admin_products'))