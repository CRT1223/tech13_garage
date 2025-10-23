#!/usr/bin/env python3
"""
Add placeholder images for team members
"""

import sqlite3
import os
from datetime import datetime

def add_team_images():
    """Add placeholder images for team members"""
    try:
        conn = sqlite3.connect('tech13_garage.db')
        cursor = conn.cursor()
        
        # Check if team_members table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team_members'")
        if not cursor.fetchone():
            print("❌ team_members table does not exist.")
            return False
        
        # Get all team members without images
        cursor.execute("SELECT id, name FROM team_members WHERE image IS NULL")
        members = cursor.fetchall()
        
        if not members:
            print("✅ All team members already have images.")
            return True
        
        # Create uploads directory if it doesn't exist
        uploads_dir = 'static/uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Add placeholder images for each member
        for member_id, name in members:
            # Create a simple placeholder image filename
            filename = f"team_{member_id}_{name.lower().replace(' ', '_')}.jpg"
            
            # Update the database with the image filename
            cursor.execute('''
                UPDATE team_members SET image = ?, updated_at = ?
                WHERE id = ?
            ''', (filename, datetime.now().isoformat(), member_id))
            
            print(f"✅ Added placeholder image for {name}: {filename}")
        
        conn.commit()
        print(f"\n✅ Updated {len(members)} team members with placeholder images")
        
        # Display updated members
        cursor.execute("SELECT name, image FROM team_members ORDER BY display_order")
        members = cursor.fetchall()
        print("\nUpdated team members:")
        for name, image in members:
            print(f"  - {name}: {image}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding team images: {e}")
        return False

if __name__ == "__main__":
    print("Adding placeholder images for team members...")
    success = add_team_images()
    if success:
        print("\n✅ Team images updated successfully!")
    else:
        print("\n❌ Failed to update team images.")
