#!/usr/bin/env python3
"""
Add sample team members to TECH13 Garage database
"""

import sqlite3
from datetime import datetime

def add_team_sample_data():
    """Add sample team members to the database"""
    try:
        conn = sqlite3.connect('tech13_garage.db')
        cursor = conn.cursor()
        
        # Check if team_members table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team_members'")
        if not cursor.fetchone():
            print("❌ team_members table does not exist. Please run the app first to create it.")
            return False
        
        # Check if team members already exist
        cursor.execute("SELECT COUNT(*) FROM team_members")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Team members already exist ({count} members). Skipping sample data.")
            return True
        
        # Sample team members data
        team_members = [
            {
                'name': 'Alex Rodriguez',
                'role': 'Founder & Lead Technician',
                'description': '15+ years of experience in motorcycle engineering and racing. Former professional racer with multiple championship titles.',
                'linkedin_url': 'https://linkedin.com/in/alex-rodriguez',
                'twitter_url': 'https://twitter.com/alex_rodriguez',
                'instagram_url': 'https://instagram.com/alex_rodriguez',
                'display_order': 1,
                'is_active': 1
            },
            {
                'name': 'Sarah Chen',
                'role': 'Head of Engineering',
                'description': 'Mechanical engineering graduate specializing in motorcycle performance optimization and custom modifications.',
                'linkedin_url': 'https://linkedin.com/in/sarah-chen',
                'twitter_url': 'https://twitter.com/sarah_chen',
                'instagram_url': 'https://instagram.com/sarah_chen',
                'display_order': 2,
                'is_active': 1
            },
            {
                'name': 'Mike Thompson',
                'role': 'Senior Technician',
                'description': 'Expert in both racing and daily motorcycle maintenance with a focus on customer satisfaction and quality service.',
                'linkedin_url': 'https://linkedin.com/in/mike-thompson',
                'twitter_url': 'https://twitter.com/mike_thompson',
                'instagram_url': 'https://instagram.com/mike_thompson',
                'display_order': 3,
                'is_active': 1
            }
        ]
        
        # Insert team members
        for member in team_members:
            cursor.execute('''
                INSERT INTO team_members (name, role, description, linkedin_url, twitter_url, instagram_url, display_order, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                member['name'],
                member['role'],
                member['description'],
                member['linkedin_url'],
                member['twitter_url'],
                member['instagram_url'],
                member['display_order'],
                member['is_active'],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        print(f"✅ Added {len(team_members)} team members to the database")
        
        # Display added members
        cursor.execute("SELECT name, role FROM team_members ORDER BY display_order")
        members = cursor.fetchall()
        print("\nAdded team members:")
        for name, role in members:
            print(f"  - {name} ({role})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding team sample data: {e}")
        return False

if __name__ == "__main__":
    print("Adding sample team members to TECH13 Garage database...")
    success = add_team_sample_data()
    if success:
        print("\n✅ Sample team data added successfully!")
    else:
        print("\n❌ Failed to add sample team data.")
