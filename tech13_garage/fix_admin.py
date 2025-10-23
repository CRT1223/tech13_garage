#!/usr/bin/env python3
import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('tech13_garage.db')
cursor = conn.cursor()

# Check if admin exists
cursor.execute('SELECT username, role FROM users WHERE role = "admin"')
admin_accounts = cursor.fetchall()
print('Current admin accounts:', admin_accounts)

# If no admin exists, create one
if not admin_accounts:
    print('No admin account found. Creating admin account...')
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT INTO users (username, email, password, first_name, last_name, role, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@tech13garage.com', admin_password, 'Admin', 'User', 'admin', '2024-01-01T00:00:00'))
    conn.commit()
    print('Admin account created successfully!')
else:
    print('Admin account already exists.')

# Verify admin account
cursor.execute('SELECT username, role FROM users WHERE role = "admin"')
admin_accounts = cursor.fetchall()
print('Admin accounts after check:', admin_accounts)

conn.close()
print('Done!')
