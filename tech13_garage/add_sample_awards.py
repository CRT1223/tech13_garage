#!/usr/bin/env python3
"""
Add sample awards to demonstrate the awards management system
"""

import sqlite3
from datetime import datetime

def add_sample_awards():
    """Add multiple sample awards to the database"""
    
    conn = sqlite3.connect('tech13_garage.db')
    cursor = conn.cursor()
    
    # Sample awards data
    sample_awards = [
        {
            'title': 'Racing Championship 2023',
            'subtitle': '1st Place - National Motorcycle Racing',
            'year': 2023,
            'category': 'Racing',
            'description': 'Won the national motorcycle racing championship with outstanding performance and technical excellence.',
            'display_order': 1,
            'is_active': 1
        },
        {
            'title': 'Best Service Award 2023',
            'subtitle': 'Excellence in Customer Service',
            'year': 2023,
            'category': 'Service',
            'description': 'Recognized for exceptional customer service and support in the motorcycle industry.',
            'display_order': 2,
            'is_active': 1
        },
        {
            'title': 'Innovation Award 2022',
            'subtitle': 'Technical Innovation in Racing',
            'year': 2022,
            'category': 'Innovation',
            'description': 'Awarded for groundbreaking technical innovations in motorcycle racing technology.',
            'display_order': 3,
            'is_active': 1
        },
        {
            'title': 'Team Championship 2023',
            'subtitle': 'Best Racing Team Performance',
            'year': 2023,
            'category': 'Team',
            'description': 'Outstanding team performance and collaboration in competitive racing events.',
            'display_order': 4,
            'is_active': 1
        },
        {
            'title': 'Quality Certification 2023',
            'subtitle': 'ISO 9001 Quality Management',
            'year': 2023,
            'category': 'Quality',
            'description': 'Achieved ISO 9001 certification for quality management systems and processes.',
            'display_order': 5,
            'is_active': 1
        },
        {
            'title': 'Safety Award 2023',
            'subtitle': 'Excellence in Safety Standards',
            'year': 2023,
            'category': 'Safety',
            'description': 'Recognized for maintaining the highest safety standards in motorcycle services.',
            'display_order': 6,
            'is_active': 1
        },
        {
            'title': 'Customer Choice 2023',
            'subtitle': 'Most Trusted Motorcycle Service',
            'year': 2023,
            'category': 'Customer',
            'description': 'Voted by customers as the most trusted motorcycle service provider.',
            'display_order': 7,
            'is_active': 1
        },
        {
            'title': 'Performance Award 2022',
            'subtitle': 'Outstanding Racing Performance',
            'year': 2022,
            'category': 'Performance',
            'description': 'Awarded for exceptional performance in competitive racing events.',
            'display_order': 8,
            'is_active': 1
        },
        {
            'title': 'Technical Excellence 2023',
            'subtitle': 'Advanced Technical Solutions',
            'year': 2023,
            'category': 'Innovation',
            'description': 'Recognized for developing advanced technical solutions in motorcycle engineering.',
            'display_order': 9,
            'is_active': 1
        },
        {
            'title': 'Community Service Award 2023',
            'subtitle': 'Outstanding Community Contribution',
            'year': 2023,
            'category': 'Other',
            'description': 'Awarded for significant contributions to the motorcycle community and local events.',
            'display_order': 10,
            'is_active': 1
        }
    ]
    
    # Insert sample awards
    for award in sample_awards:
        cursor.execute('''
            INSERT INTO awards (title, subtitle, year, category, description, display_order, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            award['title'],
            award['subtitle'],
            award['year'],
            award['category'],
            award['description'],
            award['display_order'],
            award['is_active'],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Added {len(sample_awards)} sample awards to the database!")
    print("\nSample awards added:")
    for i, award in enumerate(sample_awards, 1):
        print(f"  {i}. {award['title']} ({award['year']}) - {award['category']}")

def check_awards():
    """Check current awards in database"""
    conn = sqlite3.connect('tech13_garage.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM awards')
    count = cursor.fetchone()[0]
    print(f"\nTotal awards in database: {count}")
    
    if count > 0:
        cursor.execute('SELECT title, year, category, is_active FROM awards ORDER BY display_order, year DESC')
        awards = cursor.fetchall()
        print("\nAll awards:")
        for award in awards:
            status = "Active" if award[3] else "Inactive"
            print(f"  - {award[0]} ({award[1]}) - {award[2]} - {status}")
    
    conn.close()

if __name__ == "__main__":
    print("Adding sample awards to TECH13 Garage database...")
    add_sample_awards()
    check_awards()
    print("\n🎉 Awards system is ready! Admins can now manage awards through the admin panel.")
