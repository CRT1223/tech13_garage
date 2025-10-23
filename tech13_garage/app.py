from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
import sqlite3
import json
import os
import mimetypes
import random
import string
import csv
import datetime
from datetime import datetime
from io import StringIO
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'tech13_garage_secret_key_2024'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize SQLite database and create tables
def init_db():
    conn = None
    try:
        conn = sqlite3.connect('tech13_garage.db', timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        # Create users table for customers and admin
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                address TEXT,
                role TEXT DEFAULT 'customer',
                created_at TEXT,
                profile_image TEXT
            )
        ''')

        # Create categories table for motorcycle parts
        c.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                description TEXT,
                image TEXT
            )
        ''')

        # Create products table for motorcycle parts
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category_id INTEGER,
                brand TEXT,
                model TEXT,
                year_range TEXT,
                stock_quantity INTEGER DEFAULT 0,
                image TEXT,
                is_racing BOOLEAN DEFAULT 0,
                is_daily BOOLEAN DEFAULT 1,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        # Create services table
        c.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                duration_hours INTEGER,
                is_racing BOOLEAN DEFAULT 0,
                is_daily BOOLEAN DEFAULT 1,
                image TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Create orders table
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_number TEXT UNIQUE,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                order_date TEXT,
                delivery_address TEXT,
                phone TEXT,
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES users (id)
            )
        ''')

        # Create order_items table
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                service_id INTEGER,
                quantity INTEGER,
                price REAL,
                item_type TEXT, -- 'product' or 'service'
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')

        # Create cart table for session-based cart
        c.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                product_id INTEGER,
                service_id INTEGER,
                quantity INTEGER,
                item_type TEXT,
                created_at TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')

        # Create reviews table
        c.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                service_id INTEGER,
                rating INTEGER,
                comment TEXT,
                created_at TEXT,
                FOREIGN KEY (customer_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')

        # Create inventory_transactions table for tracking all inventory movements
        c.execute('''
            CREATE TABLE IF NOT EXISTS inventory_transactions (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                transaction_type TEXT, -- 'sale', 'walkin', 'return', 'adjustment', 'restock'
                quantity INTEGER, -- positive for additions, negative for subtractions
                order_id INTEGER, -- NULL for walk-in sales
                customer_id INTEGER, -- NULL for walk-in sales
                admin_id INTEGER, -- who processed the transaction
                notes TEXT,
                transaction_date TEXT,
                unit_price REAL,
                total_amount REAL,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (customer_id) REFERENCES users (id),
                FOREIGN KEY (admin_id) REFERENCES users (id)
            )
        ''')

        # Create walkin_sales table for tracking walk-in purchases
        c.execute('''
            CREATE TABLE IF NOT EXISTS walkin_sales (
                id INTEGER PRIMARY KEY,
                sale_number TEXT UNIQUE,
                customer_name TEXT,
                customer_phone TEXT,
                total_amount REAL,
                payment_method TEXT, -- 'cash', 'card', 'other'
                admin_id INTEGER,
                sale_date TEXT,
                notes TEXT,
                FOREIGN KEY (admin_id) REFERENCES users (id)
            )
        ''')

        # Create walkin_sale_items table
        c.execute('''
            CREATE TABLE IF NOT EXISTS walkin_sale_items (
                id INTEGER PRIMARY KEY,
                walkin_sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                total_price REAL,
                FOREIGN KEY (walkin_sale_id) REFERENCES walkin_sales (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Create team table
        c.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                description TEXT,
                image TEXT,
                linkedin_url TEXT,
                twitter_url TEXT,
                instagram_url TEXT,
                display_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Create collaborate teams table
        c.execute('''
            CREATE TABLE IF NOT EXISTS collaborate_teams (
                id INTEGER PRIMARY KEY,
                team_name TEXT NOT NULL,
                logo TEXT,
                description TEXT,
                website_url TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                partnership_type TEXT,
                is_active BOOLEAN DEFAULT 1,
                display_order INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Create awards table
        c.execute('''
            CREATE TABLE IF NOT EXISTS awards (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                subtitle TEXT,
                image TEXT,
                year INTEGER,
                category TEXT,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                display_order INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Add missing columns to existing tables
        try:
            # Add updated_at column to services table if it doesn't exist
            c.execute("ALTER TABLE services ADD COLUMN updated_at TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            # Add image column to services table if it doesn't exist
            c.execute("ALTER TABLE services ADD COLUMN image TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            # Add updated_at column to categories table if it doesn't exist
            c.execute("ALTER TABLE categories ADD COLUMN updated_at TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            # Add created_at column to categories table if it doesn't exist
            c.execute("ALTER TABLE categories ADD COLUMN created_at TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

        conn.commit()
        print("Database initialized successfully!")
        
        # Insert sample data
        insert_sample_data(c)
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def insert_sample_data(cursor):
    # Insert admin user
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password, first_name, last_name, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@tech13garage.com', admin_password, 'Admin', 'User', 'admin'))

    # Insert sample categories
    categories = [
        ('Engine Parts', 'High-performance engine components for racing and daily use'),
        ('Brake Systems', 'Brake pads, rotors, and calipers for safety and performance'),
        ('Suspension', 'Shocks, springs, and suspension components'),
        ('Exhaust Systems', 'Performance exhausts and mufflers'),
        ('Wheels & Tires', 'Racing and street wheels and tires'),
        ('Body Parts', 'Fairings, windscreens, and body components'),
        ('Electronics', 'ECU, sensors, and electronic accessories'),
        ('Maintenance', 'Oil, filters, and maintenance supplies')
    ]
    
    for cat_name, cat_desc in categories:
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, description)
            VALUES (?, ?)
        ''', (cat_name, cat_desc))

    # Insert sample products
    products = [
        ('Racing Brake Pads', 'High-performance brake pads for track use', 89.99, 2, 'Brembo', 'Racing', '2020-2024', 50, 1, 0),
        ('Street Brake Pads', 'Daily use brake pads with excellent stopping power', 45.99, 2, 'EBC', 'Street', '2018-2024', 100, 0, 1),
        ('Racing Exhaust', 'Full titanium racing exhaust system', 899.99, 4, 'Akrapovic', 'Racing', '2020-2024', 15, 1, 0),
        ('Street Exhaust', 'Stainless steel street legal exhaust', 299.99, 4, 'Yoshimura', 'Street', '2018-2024', 30, 0, 1),
        ('Racing Suspension', 'Adjustable racing suspension kit', 1299.99, 3, 'Öhlins', 'Racing', '2020-2024', 10, 1, 0),
        ('Street Suspension', 'Comfortable street suspension upgrade', 399.99, 3, 'Koni', 'Street', '2018-2024', 25, 0, 1),
        ('Racing Wheels', 'Lightweight forged racing wheels', 1599.99, 5, 'Marchesini', 'Racing', '2020-2024', 8, 1, 0),
        ('Street Wheels', 'Durable alloy street wheels', 599.99, 5, 'OZ Racing', 'Street', '2018-2024', 20, 0, 1)
    ]
    
    for product in products:
        cursor.execute('''
            INSERT OR IGNORE INTO products 
            (name, description, price, category_id, brand, model, year_range, stock_quantity, is_racing, is_daily)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', product)

    # Insert sample services
    services = [
        ('Engine Tuning', 'Professional engine tuning and mapping', 199.99, 4, 1, 0),
        ('Brake Service', 'Complete brake system inspection and service', 79.99, 2, 0, 1),
        ('Suspension Setup', 'Racing suspension tuning and setup', 149.99, 3, 1, 0),
        ('Oil Change', 'Full synthetic oil change service', 49.99, 1, 0, 1),
        ('Chain Service', 'Chain cleaning, lubrication, and adjustment', 39.99, 1, 0, 1),
        ('Racing Preparation', 'Complete racing bike preparation', 299.99, 6, 1, 0),
        ('Safety Inspection', 'Comprehensive safety inspection', 59.99, 2, 0, 1),
        ('Performance Upgrade', 'Performance parts installation and tuning', 199.99, 4, 1, 0)
    ]
    
    for service in services:
        cursor.execute('''
            INSERT OR IGNORE INTO services 
            (name, description, price, duration_hours, is_racing, is_daily)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', service)

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('tech13_garage.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('role') == 'admin'

def generate_order_number():
    return f"TECH13-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

def generate_sale_number():
    return f"WALKIN-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

def record_inventory_transaction(product_id, transaction_type, quantity, order_id=None, customer_id=None, admin_id=None, notes="", unit_price=0, total_amount=0):
    """Record inventory transaction"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO inventory_transactions 
        (product_id, transaction_type, quantity, order_id, customer_id, admin_id, notes, transaction_date, unit_price, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (product_id, transaction_type, quantity, order_id, customer_id, admin_id, notes, datetime.now().isoformat(), unit_price, total_amount))
    conn.commit()
    conn.close()

def update_product_stock(product_id, quantity_change):
    """Update product stock quantity"""
    conn = get_db_connection()
    conn.execute('''
        UPDATE products SET stock_quantity = stock_quantity + ? WHERE id = ?
    ''', (quantity_change, product_id))
    conn.commit()
    conn.close()

# Initialize database on app startup
init_db()

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get featured products
    featured_products = conn.execute('''
        SELECT * FROM products WHERE stock_quantity > 0 
        ORDER BY created_at DESC LIMIT 8
    ''').fetchall()
    
    # Get categories
    categories = conn.execute('SELECT * FROM categories').fetchall()
    
    # Get services
    services = conn.execute('SELECT * FROM services').fetchall()
    
    # Get awards
    awards = conn.execute('''
        SELECT * FROM awards 
        WHERE is_active = 1 
        ORDER BY display_order, year DESC, title
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         featured_products=featured_products,
                         categories=categories,
                         services=services,
                         awards=awards)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('''
            SELECT * FROM users WHERE username = ? OR email = ?
        ''', (username, username)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['first_name'] = user['first_name']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        
        # Check if username or email already exists
        existing_user = conn.execute('''
            SELECT * FROM users WHERE username = ? OR email = ?
        ''', (username, email)).fetchone()
        
        if existing_user:
            flash('Username or email already exists', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        conn.execute('''
            INSERT INTO users (username, email, password, first_name, last_name, phone, address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, hashed_password, first_name, last_name, phone, address, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/products')
def products():
    category_id = request.args.get('category')
    product_type = request.args.get('type')  # racing or daily
    search = request.args.get('search')
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM products WHERE stock_quantity > 0'
    params = []
    
    if category_id:
        query += ' AND category_id = ?'
        params.append(category_id)
    
    if product_type == 'racing':
        query += ' AND is_racing = 1'
    elif product_type == 'daily':
        query += ' AND is_daily = 1'
    
    if search:
        query += ' AND (name LIKE ? OR description LIKE ? OR brand LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    
    query += ' ORDER BY created_at DESC'
    
    products = conn.execute(query, params).fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    
    conn.close()
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category_id,
                         selected_type=product_type,
                         search_term=search)

@app.route('/services')
def services():
    service_type = request.args.get('type')  # racing or daily
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM services'
    params = []
    
    if service_type == 'racing':
        query += ' WHERE is_racing = 1'
    elif service_type == 'daily':
        query += ' WHERE is_daily = 1'
    
    query += ' ORDER BY name'
    
    services = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('services.html', 
                         services=services,
                         selected_type=service_type)

@app.route('/about')
def about():
    conn = get_db_connection()
    team_members = conn.execute('''
        SELECT * FROM team_members 
        WHERE is_active = 1 
        ORDER BY display_order, name
    ''').fetchall()
    
    collaborate_teams = conn.execute('''
        SELECT * FROM collaborate_teams 
        WHERE is_active = 1 
        ORDER BY display_order, team_name
    ''').fetchall()
    conn.close()
    
    return render_template('about.html', team_members=team_members, collaborate_teams=collaborate_teams)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('products'))
    
    # Get related products
    related_products = conn.execute('''
        SELECT * FROM products 
        WHERE category_id = ? AND id != ? AND stock_quantity > 0
        LIMIT 4
    ''', (product['category_id'], product_id)).fetchall()
    
    # Get reviews
    reviews = conn.execute('''
        SELECT r.*, u.first_name, u.last_name 
        FROM reviews r 
        JOIN users u ON r.customer_id = u.id 
        WHERE r.product_id = ?
        ORDER BY r.created_at DESC
    ''', (product_id,)).fetchall()
    
    conn.close()
    
    return render_template('product_detail.html', 
                         product=product,
                         related_products=related_products,
                         reviews=reviews)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not is_logged_in():
        return jsonify({'success': False, 'message': 'Please login to add items to cart'})
    
    # Check if user is admin - admins cannot add items to cart
    if is_admin():
        return jsonify({'success': False, 'message': 'Administrators cannot add items to cart. Please use a customer account.'})
    
    product_id = request.form.get('product_id')
    service_id = request.form.get('service_id')
    quantity = int(request.form.get('quantity', 1))
    item_type = 'product' if product_id else 'service'
    
    conn = get_db_connection()
    
    # Check if item exists in cart
    existing_item = conn.execute('''
        SELECT * FROM cart 
        WHERE session_id = ? AND product_id = ? AND service_id = ? AND item_type = ?
    ''', (session['user_id'], product_id, service_id, item_type)).fetchone()
    
    if existing_item:
        # Update quantity
        conn.execute('''
            UPDATE cart SET quantity = quantity + ? 
            WHERE id = ?
        ''', (quantity, existing_item['id']))
    else:
        # Add new item
        conn.execute('''
            INSERT INTO cart (session_id, product_id, service_id, quantity, item_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], product_id, service_id, quantity, item_type, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Item added to cart'})

@app.route('/cart')
def cart():
    if not is_logged_in():
        flash('Please login to view cart', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    cart_items = conn.execute('''
        SELECT c.*, p.name as product_name, p.price as product_price, p.image as product_image,
               s.name as service_name, s.price as service_price
        FROM cart c
        LEFT JOIN products p ON c.product_id = p.id
        LEFT JOIN services s ON c.service_id = s.id
        WHERE c.session_id = ?
        ORDER BY c.created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('cart.html', cart_items=cart_items)

@app.route('/remove_from_cart/<int:cart_id>')
def remove_from_cart(cart_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM cart WHERE id = ? AND session_id = ?', (cart_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        delivery_address = request.form['delivery_address']
        phone = request.form['phone']
        notes = request.form.get('notes', '')
        
        conn = get_db_connection()
        
        # Get cart items
        cart_items = conn.execute('''
            SELECT c.*, p.name as product_name, p.price as product_price,
                   s.name as service_name, s.price as service_price
            FROM cart c
            LEFT JOIN products p ON c.product_id = p.id
            LEFT JOIN services s ON c.service_id = s.id
            WHERE c.session_id = ?
        ''', (session['user_id'],)).fetchall()
        
        if not cart_items:
            flash('Your cart is empty', 'error')
            return redirect(url_for('cart'))
        
        # Calculate total
        total_amount = sum(
            (item['product_price'] or item['service_price'] or 0) * item['quantity'] 
            for item in cart_items
        )
        
        # Create order
        order_number = generate_order_number()
        conn.execute('''
            INSERT INTO orders (customer_id, order_number, total_amount, delivery_address, phone, notes, order_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], order_number, total_amount, delivery_address, phone, notes, datetime.now().isoformat()))
        
        order_id = conn.lastrowid
        
        # Create order items
        for item in cart_items:
            conn.execute('''
                INSERT INTO order_items (order_id, product_id, service_id, quantity, price, item_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['service_id'], item['quantity'], 
                  item['product_price'] or item['service_price'] or 0, item['item_type']))
            
            # Update stock for products and record inventory transaction
            if item['product_id']:
                conn.execute('''
                    UPDATE products SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                ''', (item['quantity'], item['product_id']))
                
                # Record inventory transaction
                record_inventory_transaction(
                    product_id=item['product_id'],
                    transaction_type='sale',
                    quantity=-item['quantity'],  # Negative for sales
                    order_id=order_id,
                    customer_id=session['user_id'],
                    admin_id=None,  # Online order
                    notes=f"Online order {order_number}",
                    unit_price=item['product_price'] or 0,
                    total_amount=(item['product_price'] or 0) * item['quantity']
                )
        
        # Clear cart
        conn.execute('DELETE FROM cart WHERE session_id = ?', (session['user_id'],))
        
        conn.commit()
        conn.close()
        
        flash(f'Order placed successfully! Order number: {order_number}', 'success')
        return redirect(url_for('order_history'))
    
    # Get user info for checkout form
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('checkout.html', user=user)

@app.route('/order_history')
def order_history():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT * FROM orders 
        WHERE customer_id = ? 
        ORDER BY order_date DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('order_history.html', orders=orders)

@app.route('/order/<int:order_id>')
def order_detail(order_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get order details
    order = conn.execute('''
        SELECT * FROM orders WHERE id = ? AND customer_id = ?
    ''', (order_id, session['user_id'])).fetchone()
    
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('order_history'))
    
    # Get order items
    order_items = conn.execute('''
        SELECT oi.*, p.name as product_name, p.image as product_image,
               s.name as service_name
        FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.id
        LEFT JOIN services s ON oi.service_id = s.id
        WHERE oi.order_id = ?
    ''', (order_id,)).fetchall()
    
    conn.close()
    
    return render_template('order_detail.html', order=order, order_items=order_items)

# Admin routes
@app.route('/admin')
def admin_dashboard():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get statistics
    total_products = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()['count']
    total_orders = conn.execute('SELECT COUNT(*) as count FROM orders').fetchone()['count']
    total_customers = conn.execute('SELECT COUNT(*) as count FROM users WHERE role = "customer"').fetchone()['count']
    total_revenue = conn.execute('SELECT SUM(total_amount) as total FROM orders WHERE status = "completed"').fetchone()['total']
    total_revenue = total_revenue if total_revenue is not None else 0
    
    # Get recent orders
    recent_orders = conn.execute('''
        SELECT o.*, u.first_name, u.last_name 
        FROM orders o 
        JOIN users u ON o.customer_id = u.id 
        ORDER BY o.order_date DESC 
        LIMIT 10
    ''').fetchall()
    
    # Get low stock products
    low_stock = conn.execute('''
        SELECT * FROM products WHERE stock_quantity < 10
        ORDER BY stock_quantity ASC
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_customers=total_customers,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         low_stock=low_stock)

@app.route('/admin/products')
def admin_products():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    products = conn.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        ORDER BY p.created_at DESC
    ''').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    return render_template('admin/products.html', products=products, categories=categories)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        brand = request.form['brand']
        model = request.form['model']
        year_range = request.form['year_range']
        stock_quantity = int(request.form['stock_quantity'])
        is_racing = 'is_racing' in request.form
        is_daily = 'is_daily' in request.form
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO products (name, description, price, category_id, brand, model, year_range, 
                                stock_quantity, image, is_racing, is_daily, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, price, category_id, brand, model, year_range, 
              stock_quantity, image, is_racing, is_daily, 
              datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_products'))
    
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/orders')
def admin_orders():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, u.first_name, u.last_name, u.email 
        FROM orders o 
        JOIN users u ON o.customer_id = u.id 
        ORDER BY o.order_date DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/orders/<int:order_id>/update_status', methods=['POST'])
def admin_update_order_status(order_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    new_status = request.form['status']
    
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
    conn.commit()
    conn.close()
    
    flash('Order status updated successfully', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/admin/customers')
def admin_customers():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    customers = conn.execute('''
        SELECT * FROM users WHERE role = 'customer' ORDER BY created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/customers.html', customers=customers)

@app.route('/admin/inventory')
def admin_inventory():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get inventory summary
    inventory_summary = conn.execute('''
        SELECT p.id, p.name, p.brand, p.model, p.stock_quantity, p.price,
               c.name as category_name,
               COALESCE(sold.total_sold, 0) as total_sold,
               COALESCE(walkin.total_walkin, 0) as total_walkin
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN (
            SELECT product_id, SUM(ABS(quantity)) as total_sold
            FROM inventory_transactions 
            WHERE transaction_type = 'sale'
            GROUP BY product_id
        ) sold ON p.id = sold.product_id
        LEFT JOIN (
            SELECT product_id, SUM(ABS(quantity)) as total_walkin
            FROM inventory_transactions 
            WHERE transaction_type = 'walkin'
            GROUP BY product_id
        ) walkin ON p.id = walkin.product_id
        ORDER BY p.name
    ''').fetchall()
    
    # Get recent inventory transactions
    recent_transactions = conn.execute('''
        SELECT it.*, p.name as product_name, p.brand, p.model,
               u.first_name, u.last_name, o.order_number
        FROM inventory_transactions it
        JOIN products p ON it.product_id = p.id
        LEFT JOIN users u ON it.admin_id = u.id
        LEFT JOIN orders o ON it.order_id = o.id
        ORDER BY it.transaction_date DESC
        LIMIT 50
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin/inventory.html', 
                         inventory_summary=inventory_summary,
                         recent_transactions=recent_transactions)

@app.route('/admin/walkin-sales')
def admin_walkin_sales():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    walkin_sales = conn.execute('''
        SELECT ws.*, u.first_name, u.last_name
        FROM walkin_sales ws
        LEFT JOIN users u ON ws.admin_id = u.id
        ORDER BY ws.sale_date DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/walkin_sales.html', walkin_sales=walkin_sales)

@app.route('/admin/walkin-sales/new', methods=['GET', 'POST'])
def admin_new_walkin_sale():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form.get('customer_phone', '')
        payment_method = request.form['payment_method']
        notes = request.form.get('notes', '')
        
        # Get product data from form
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        
        if not product_ids or not any(quantities):
            flash('Please add at least one product', 'error')
            return redirect(url_for('admin_new_walkin_sale'))
        
        conn = get_db_connection()
        
        # Calculate total amount
        total_amount = 0
        sale_items = []
        
        for i, product_id in enumerate(product_ids):
            if quantities[i] and int(quantities[i]) > 0:
                product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
                if product and product['stock_quantity'] >= int(quantities[i]):
                    quantity = int(quantities[i])
                    unit_price = product['price'] or 0
                    item_total = unit_price * quantity
                    total_amount += item_total
                    
                    sale_items.append({
                        'product_id': product_id,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': item_total,
                        'product_name': product['name']
                    })
        
        if not sale_items:
            flash('No valid products selected', 'error')
            conn.close()
            return redirect(url_for('admin_new_walkin_sale'))
        
        # Create walk-in sale
        sale_number = generate_sale_number()
        conn.execute('''
            INSERT INTO walkin_sales (sale_number, customer_name, customer_phone, total_amount, payment_method, admin_id, sale_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sale_number, customer_name, customer_phone, total_amount, payment_method, session['user_id'], datetime.now().isoformat(), notes))
        
        sale_id = conn.lastrowid
        
        # Create sale items and update inventory
        for item in sale_items:
            conn.execute('''
                INSERT INTO walkin_sale_items (walkin_sale_id, product_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (sale_id, item['product_id'], item['quantity'], item['unit_price'], item['total_price']))
            
            # Update stock
            conn.execute('''
                UPDATE products SET stock_quantity = stock_quantity - ?
                WHERE id = ?
            ''', (item['quantity'], item['product_id']))
            
            # Record inventory transaction
            record_inventory_transaction(
                product_id=item['product_id'],
                transaction_type='walkin',
                quantity=-item['quantity'],
                order_id=None,
                customer_id=None,
                admin_id=session['user_id'],
                notes=f"Walk-in sale {sale_number}",
                unit_price=item['unit_price'],
                total_amount=item['total_price']
            )
        
        conn.commit()
        conn.close()
        
        flash(f'Walk-in sale completed! Sale number: {sale_number}', 'success')
        return redirect(url_for('admin_walkin_sales'))
    
    # Get all products for selection
    conn = get_db_connection()
    products = conn.execute('''
        SELECT * FROM products WHERE stock_quantity > 0 ORDER BY name
    ''').fetchall()
    conn.close()
    
    return render_template('admin/new_walkin_sale.html', products=products)

@app.route('/admin/inventory/restock', methods=['POST'])
def admin_restock_inventory():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    notes = request.form.get('notes', '')
    
    if quantity <= 0:
        flash('Quantity must be positive', 'error')
        return redirect(url_for('admin_inventory'))
    
    conn = get_db_connection()
    
    # Update stock
    conn.execute('''
        UPDATE products SET stock_quantity = stock_quantity + ?
        WHERE id = ?
    ''', (quantity, product_id))
    
    # Record inventory transaction
    record_inventory_transaction(
        product_id=product_id,
        transaction_type='restock',
        quantity=quantity,
        admin_id=session['user_id'],
        notes=notes or f"Restocked {quantity} units"
    )
    
    conn.commit()
    conn.close()
    
    flash('Inventory restocked successfully', 'success')
    return redirect(url_for('admin_inventory'))

@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    if not is_logged_in():
        return jsonify({'success': False, 'message': 'Please login'})
    
    cart_id = request.form.get('cart_id')
    quantity = int(request.form.get('quantity', 1))
    
    conn = get_db_connection()
    conn.execute('UPDATE cart SET quantity = ? WHERE id = ? AND session_id = ?', 
                (quantity, cart_id, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Quantity updated'})

# Additional Admin Routes for Full Functionality

@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        brand = request.form['brand']
        model = request.form['model']
        year_range = request.form['year_range']
        stock_quantity = int(request.form['stock_quantity'])
        is_racing = 'is_racing' in request.form
        is_daily = 'is_daily' in request.form
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        # Update product
        if image:
            conn.execute('''
                UPDATE products SET name = ?, description = ?, price = ?, category_id = ?, 
                                  brand = ?, model = ?, year_range = ?, stock_quantity = ?, 
                                  image = ?, is_racing = ?, is_daily = ?, updated_at = ?
                WHERE id = ?
            ''', (name, description, price, category_id, brand, model, year_range, 
                  stock_quantity, image, is_racing, is_daily, datetime.now().isoformat(), product_id))
        else:
            conn.execute('''
                UPDATE products SET name = ?, description = ?, price = ?, category_id = ?, 
                                  brand = ?, model = ?, year_range = ?, stock_quantity = ?, 
                                  is_racing = ?, is_daily = ?, updated_at = ?
                WHERE id = ?
            ''', (name, description, price, category_id, brand, model, year_range, 
                  stock_quantity, is_racing, is_daily, datetime.now().isoformat(), product_id))
        
        conn.commit()
        conn.close()
        
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_products'))
    
    # Get product data for editing
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/<int:product_id>/delete', methods=['POST'])
def admin_delete_product(product_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Check if product exists
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if not product:
        flash('Product not found', 'error')
        conn.close()
        return redirect(url_for('admin_products'))
    
    # Check if product is in any orders
    order_items = conn.execute('''
        SELECT COUNT(*) as count FROM order_items WHERE product_id = ?
    ''', (product_id,)).fetchone()
    
    if order_items['count'] > 0:
        flash('Cannot delete product that has been ordered. Consider marking as discontinued instead.', 'error')
        conn.close()
        return redirect(url_for('admin_products'))
    
    # Delete product image if exists
    if product['image']:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product['image']))
        except:
            pass  # Ignore if file doesn't exist
    
    # Delete product
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/categories')
def admin_categories():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
def admin_add_category():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO categories (name, description, created_at)
            VALUES (?, ?, ?)
        ''', (name, description, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        flash('Category added successfully', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/add_category.html')

@app.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def admin_edit_category(category_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        conn.execute('''
            UPDATE categories SET name = ?, description = ?, updated_at = ?
            WHERE id = ?
        ''', (name, description, datetime.now().isoformat(), category_id))
        conn.commit()
        conn.close()
        
        flash('Category updated successfully', 'success')
        return redirect(url_for('admin_categories'))
    
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    conn.close()
    
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
def admin_delete_category(category_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Check if category has products
    products = conn.execute('SELECT COUNT(*) as count FROM products WHERE category_id = ?', (category_id,)).fetchone()
    if products['count'] > 0:
        flash('Cannot delete category that has products. Please move or delete products first.', 'error')
        conn.close()
        return redirect(url_for('admin_categories'))
    
    conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    
    flash('Category deleted successfully', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/services')
def admin_services():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services ORDER BY name').fetchall()
    conn.close()
    
    return render_template('admin/services.html', services=services)

@app.route('/admin/services/add', methods=['GET', 'POST'])
def admin_add_service():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        is_racing = 'is_racing' in request.form
        is_daily = 'is_daily' in request.form
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO services (name, description, price, is_racing, is_daily, image, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, price, is_racing, is_daily, image, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        flash('Service added successfully', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/add_service.html')

@app.route('/admin/services/<int:service_id>/edit', methods=['GET', 'POST'])
def admin_edit_service(service_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        is_racing = 'is_racing' in request.form
        is_daily = 'is_daily' in request.form
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        # Update service
        if image:
            conn.execute('''
                UPDATE services SET name = ?, description = ?, price = ?, is_racing = ?, is_daily = ?, image = ?, updated_at = ?
                WHERE id = ?
            ''', (name, description, price, is_racing, is_daily, image, datetime.now().isoformat(), service_id))
        else:
            conn.execute('''
                UPDATE services SET name = ?, description = ?, price = ?, is_racing = ?, is_daily = ?, updated_at = ?
                WHERE id = ?
            ''', (name, description, price, is_racing, is_daily, datetime.now().isoformat(), service_id))
        
        conn.commit()
        conn.close()
        
        flash('Service updated successfully', 'success')
        return redirect(url_for('admin_services'))
    
    service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
    conn.close()
    
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/edit_service.html', service=service)

# Team Management Routes
@app.route('/admin/team')
def admin_team():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    team_members = conn.execute('''
        SELECT * FROM team_members 
        ORDER BY display_order, name
    ''').fetchall()
    conn.close()
    
    return render_template('admin/team.html', team_members=team_members)

@app.route('/admin/team/add', methods=['GET', 'POST'])
def admin_add_team_member():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        description = request.form['description']
        linkedin_url = request.form.get('linkedin_url', '')
        twitter_url = request.form.get('twitter_url', '')
        instagram_url = request.form.get('instagram_url', '')
        display_order = int(request.form.get('display_order', 0))
        is_active = 'is_active' in request.form
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO team_members (name, role, description, image, linkedin_url, twitter_url, instagram_url, display_order, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, role, description, image, linkedin_url, twitter_url, instagram_url, display_order, is_active, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        flash('Team member added successfully', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/add_team_member.html')

@app.route('/admin/team/<int:member_id>/edit', methods=['GET', 'POST'])
def admin_edit_team_member(member_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        description = request.form['description']
        linkedin_url = request.form.get('linkedin_url', '')
        twitter_url = request.form.get('twitter_url', '')
        instagram_url = request.form.get('instagram_url', '')
        display_order = int(request.form.get('display_order', 0))
        is_active = 'is_active' in request.form
        
        # Handle file upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        # Update team member
        if image:
            conn.execute('''
                UPDATE team_members SET name = ?, role = ?, description = ?, image = ?, linkedin_url = ?, twitter_url = ?, instagram_url = ?, display_order = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            ''', (name, role, description, image, linkedin_url, twitter_url, instagram_url, display_order, is_active, datetime.now().isoformat(), member_id))
        else:
            conn.execute('''
                UPDATE team_members SET name = ?, role = ?, description = ?, linkedin_url = ?, twitter_url = ?, instagram_url = ?, display_order = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            ''', (name, role, description, linkedin_url, twitter_url, instagram_url, display_order, is_active, datetime.now().isoformat(), member_id))
        
        conn.commit()
        conn.close()
        
        flash('Team member updated successfully', 'success')
        return redirect(url_for('admin_team'))
    
    team_member = conn.execute('SELECT * FROM team_members WHERE id = ?', (member_id,)).fetchone()
    conn.close()
    
    if not team_member:
        flash('Team member not found', 'error')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/edit_team_member.html', team_member=team_member)

@app.route('/admin/team/<int:member_id>/delete', methods=['POST'])
def admin_delete_team_member(member_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM team_members WHERE id = ?', (member_id,))
    conn.commit()
    conn.close()
    
    flash('Team member deleted successfully', 'success')
    return redirect(url_for('admin_team'))

@app.route('/admin/team/<int:member_id>/update-image', methods=['POST'])
def admin_update_team_member_image(member_id):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file provided'})
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE team_members SET image = ?, updated_at = ?
            WHERE id = ?
        ''', (filename, datetime.now().isoformat(), member_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Image updated successfully',
            'image_url': url_for('static', filename='uploads/' + filename)
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid file format'})

# Collaborate Teams Admin Routes
@app.route('/admin/collaborate-teams')
def admin_collaborate_teams():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    collaborate_teams = conn.execute('''
        SELECT * FROM collaborate_teams 
        ORDER BY display_order, team_name
    ''').fetchall()
    conn.close()
    
    return render_template('admin/collaborate_teams.html', collaborate_teams=collaborate_teams)

@app.route('/admin/collaborate-teams/add', methods=['GET', 'POST'])
def admin_add_collaborate_team():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        team_name = request.form['team_name']
        description = request.form['description']
        website_url = request.form['website_url']
        contact_email = request.form['contact_email']
        contact_phone = request.form['contact_phone']
        partnership_type = request.form['partnership_type']
        display_order = int(request.form.get('display_order', 0))
        is_active = 'is_active' in request.form
        
        # Handle logo upload
        logo = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO collaborate_teams (team_name, logo, description, website_url, contact_email, contact_phone, partnership_type, display_order, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (team_name, logo, description, website_url, contact_email, contact_phone, partnership_type, display_order, is_active, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        flash('Collaborate team added successfully', 'success')
        return redirect(url_for('admin_collaborate_teams'))
    
    return render_template('admin/add_collaborate_team.html')

@app.route('/admin/collaborate-teams/<int:team_id>/edit', methods=['GET', 'POST'])
def admin_edit_collaborate_team(team_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        team_name = request.form['team_name']
        description = request.form['description']
        website_url = request.form['website_url']
        contact_email = request.form['contact_email']
        contact_phone = request.form['contact_phone']
        partnership_type = request.form['partnership_type']
        display_order = int(request.form.get('display_order', 0))
        is_active = 'is_active' in request.form
        
        # Handle logo upload
        logo = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename
        
        if logo:
            conn.execute('''
                UPDATE collaborate_teams SET team_name = ?, logo = ?, description = ?, website_url = ?, contact_email = ?, contact_phone = ?, partnership_type = ?, display_order = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            ''', (team_name, logo, description, website_url, contact_email, contact_phone, partnership_type, display_order, is_active, datetime.now().isoformat(), team_id))
        else:
            conn.execute('''
                UPDATE collaborate_teams SET team_name = ?, description = ?, website_url = ?, contact_email = ?, contact_phone = ?, partnership_type = ?, display_order = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            ''', (team_name, description, website_url, contact_email, contact_phone, partnership_type, display_order, is_active, datetime.now().isoformat(), team_id))
        
        conn.commit()
        conn.close()
        
        flash('Collaborate team updated successfully', 'success')
        return redirect(url_for('admin_collaborate_teams'))
    
    team = conn.execute('SELECT * FROM collaborate_teams WHERE id = ?', (team_id,)).fetchone()
    conn.close()
    
    if not team:
        flash('Collaborate team not found', 'error')
        return redirect(url_for('admin_collaborate_teams'))
    
    return render_template('admin/edit_collaborate_team.html', team=team)

@app.route('/admin/collaborate-teams/<int:team_id>/delete', methods=['POST'])
def admin_delete_collaborate_team(team_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM collaborate_teams WHERE id = ?', (team_id,))
    conn.commit()
    conn.close()
    
    flash('Collaborate team deleted successfully', 'success')
    return redirect(url_for('admin_collaborate_teams'))

@app.route('/admin/collaborate-teams/<int:team_id>/update-logo', methods=['POST'])
def admin_update_collaborate_team_logo(team_id):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    if 'logo' not in request.files:
        return jsonify({'success': False, 'message': 'No logo file provided'})
    
    file = request.files['logo']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE collaborate_teams SET logo = ?, updated_at = ?
            WHERE id = ?
        ''', (filename, datetime.now().isoformat(), team_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Logo updated successfully',
            'logo_url': url_for('static', filename='uploads/' + filename)
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid file format'})

# Awards Admin Routes
@app.route('/admin/awards')
def admin_awards():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    awards = conn.execute('''
        SELECT * FROM awards 
        ORDER BY display_order, year DESC, title
    ''').fetchall()
    conn.close()
    
    return render_template('admin/awards.html', awards=awards)

@app.route('/admin/awards/add', methods=['GET', 'POST'])
def admin_add_award():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        year = int(request.form['year'])
        category = request.form['category']
        description = request.form['description']
        display_order = int(request.form.get('display_order', 0))
        is_active = 'is_active' in request.form
        
        # Handle image upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO awards (title, subtitle, image, year, category, description, display_order, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, subtitle, image, year, category, description, display_order, is_active, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        flash('Award added successfully', 'success')
        return redirect(url_for('admin_awards'))
    
    return render_template('admin/add_award.html')

@app.route('/admin/awards/<int:award_id>/edit', methods=['GET', 'POST'])
def admin_edit_award(award_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        year = int(request.form['year'])
        category = request.form['category']
        description = request.form['description']
        display_order = int(request.form.get('display_order', 0))
        is_active = 'is_active' in request.form
        
        # Handle image upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        if image:
            conn.execute('''
                UPDATE awards SET title = ?, subtitle = ?, image = ?, year = ?, category = ?, description = ?, display_order = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            ''', (title, subtitle, image, year, category, description, display_order, is_active, datetime.now().isoformat(), award_id))
        else:
            conn.execute('''
                UPDATE awards SET title = ?, subtitle = ?, year = ?, category = ?, description = ?, display_order = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            ''', (title, subtitle, year, category, description, display_order, is_active, datetime.now().isoformat(), award_id))
        
        conn.commit()
        conn.close()
        
        flash('Award updated successfully', 'success')
        return redirect(url_for('admin_awards'))
    
    award = conn.execute('SELECT * FROM awards WHERE id = ?', (award_id,)).fetchone()
    conn.close()
    
    if not award:
        flash('Award not found', 'error')
        return redirect(url_for('admin_awards'))
    
    return render_template('admin/edit_award.html', award=award)

@app.route('/admin/awards/<int:award_id>/delete', methods=['POST'])
def admin_delete_award(award_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM awards WHERE id = ?', (award_id,))
    conn.commit()
    conn.close()
    
    flash('Award deleted successfully', 'success')
    return redirect(url_for('admin_awards'))

@app.route('/admin/awards/<int:award_id>/update-image', methods=['POST'])
def admin_update_award_image(award_id):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file provided'})
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE awards SET image = ?, updated_at = ?
            WHERE id = ?
        ''', (filename, datetime.now().isoformat(), award_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Image updated successfully',
            'image_url': url_for('static', filename='uploads/' + filename)
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid file format'})

@app.route('/admin/services/<int:service_id>/delete', methods=['POST'])
def admin_delete_service(service_id):
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Check if service is in any orders
    order_items = conn.execute('''
        SELECT COUNT(*) as count FROM order_items WHERE service_id = ?
    ''', (service_id,)).fetchone()
    
    if order_items['count'] > 0:
        flash('Cannot delete service that has been ordered.', 'error')
        conn.close()
        return redirect(url_for('admin_services'))
    
    conn.execute('DELETE FROM services WHERE id = ?', (service_id,))
    conn.commit()
    conn.close()
    
    flash('Service deleted successfully', 'success')
    return redirect(url_for('admin_services'))

# AJAX route for updating service image in real-time
@app.route('/admin/services/<int:service_id>/update-image', methods=['POST'])
def admin_update_service_image(service_id):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file provided'})
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE services SET image = ?, updated_at = ?
            WHERE id = ?
        ''', (filename, datetime.now().isoformat(), service_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Image updated successfully',
            'image_url': url_for('static', filename='uploads/' + filename)
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid file format'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
