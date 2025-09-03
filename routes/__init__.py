from flask import Blueprint

# Import all blueprints
import auth
import products
import orders
import admin

# List of all blueprints to register
all_blueprints = [
    auth.bp,
    products.bp,
    orders.bp,
    admin.bp
] 