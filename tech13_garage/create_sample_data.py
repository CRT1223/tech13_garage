#!/usr/bin/env python3
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_sample_data():
    conn = sqlite3.connect('tech13_garage.db')
    cursor = conn.cursor()
    
    # Insert admin user
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password, first_name, last_name, role, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@tech13garage.com', admin_password, 'Admin', 'User', 'admin', datetime.now().isoformat()))

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

    # Insert sample products (prices in Philippine Peso)
    products = [
        ('Racing Brake Pads', 'High-performance brake pads for track use', 4500.00, 2, 'Brembo', 'Racing', '2020-2024', 50, 1, 0),
        ('Street Brake Pads', 'Daily use brake pads with excellent stopping power', 2300.00, 2, 'EBC', 'Street', '2018-2024', 100, 0, 1),
        ('Racing Exhaust', 'Full titanium racing exhaust system', 45000.00, 4, 'Akrapovic', 'Racing', '2020-2024', 15, 1, 0),
        ('Street Exhaust', 'Stainless steel street legal exhaust', 15000.00, 4, 'Yoshimura', 'Street', '2018-2024', 30, 0, 1),
        ('Racing Suspension', 'Adjustable racing suspension kit', 65000.00, 3, 'Öhlins', 'Racing', '2020-2024', 10, 1, 0),
        ('Street Suspension', 'Comfortable street suspension upgrade', 20000.00, 3, 'Koni', 'Street', '2018-2024', 25, 0, 1),
        ('Racing Wheels', 'Lightweight forged racing wheels', 80000.00, 5, 'Marchesini', 'Racing', '2020-2024', 8, 1, 0),
        ('Street Wheels', 'Durable alloy street wheels', 30000.00, 5, 'OZ Racing', 'Street', '2018-2024', 20, 0, 1),
        ('Racing Chain', 'High-performance racing chain', 10000.00, 1, 'DID', 'Racing', '2020-2024', 25, 1, 0),
        ('Street Chain', 'Durable street chain', 4500.00, 1, 'RK', 'Street', '2018-2024', 40, 0, 1)
    ]
    
    for product in products:
        cursor.execute('''
            INSERT OR IGNORE INTO products 
            (name, description, price, category_id, brand, model, year_range, stock_quantity, is_racing, is_daily, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*product, datetime.now().isoformat(), datetime.now().isoformat()))

    # Insert sample services (prices in Philippine Peso)
    services = [
        ('Engine Tuning', 'Professional engine tuning and mapping', 10000.00, 4, 1, 0),
        ('Brake Service', 'Complete brake system inspection and service', 4000.00, 2, 0, 1),
        ('Suspension Setup', 'Racing suspension tuning and setup', 7500.00, 3, 1, 0),
        ('Oil Change', 'Full synthetic oil change service', 2500.00, 1, 0, 1),
        ('Chain Service', 'Chain cleaning, lubrication, and adjustment', 2000.00, 1, 0, 1),
        ('Racing Preparation', 'Complete racing bike preparation', 15000.00, 6, 1, 0),
        ('Safety Inspection', 'Comprehensive safety inspection', 3000.00, 2, 0, 1),
        ('Performance Upgrade', 'Performance parts installation and tuning', 10000.00, 4, 1, 0)
    ]
    
    for service in services:
        cursor.execute('''
            INSERT OR IGNORE INTO services 
            (name, description, price, duration_hours, is_racing, is_daily, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (*service, datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print('Sample data created successfully!')

if __name__ == '__main__':
    create_sample_data()
