#!/usr/bin/env python3
"""
Test script for TECH13 Garage application
"""

import sqlite3
import os
import sys

def test_database():
    """Test database connection and tables"""
    print("Testing database...")
    
    if not os.path.exists('tech13_garage.db'):
        print("❌ Database file not found. Run the app first to create it.")
        return False
    
    try:
        conn = sqlite3.connect('tech13_garage.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        expected_tables = ['users', 'categories', 'products', 'services', 'orders', 'order_items', 'cart', 'reviews']
        existing_tables = [table[0] for table in tables]
        
        print(f"Found tables: {existing_tables}")
        
        for table in expected_tables:
            if table in existing_tables:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
                return False
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Users in database: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"✅ Products in database: {product_count}")
        
        cursor.execute("SELECT COUNT(*) FROM services")
        service_count = cursor.fetchone()[0]
        print(f"✅ Services in database: {service_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import werkzeug
        print("✅ Werkzeug imported successfully")
    except ImportError:
        print("❌ Werkzeug not installed")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/products.html',
        'templates/services.html',
        'templates/cart.html',
        'templates/checkout.html',
        'templates/order_history.html',
        'templates/order_detail.html',
        'templates/profile.html',
        'templates/admin/dashboard.html',
        'templates/admin/products.html',
        'templates/admin/add_product.html',
        'templates/admin/orders.html',
        'templates/admin/customers.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 50)
    print("TECH13 GARAGE APPLICATION TEST")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Database", test_database)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("1. cd tech13_garage")
        print("2. python app.py")
        print("3. Open http://localhost:5000 in your browser")
        print("4. Admin login: username=admin, password=admin123")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
