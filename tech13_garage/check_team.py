#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('tech13_garage.db')
cursor = conn.cursor()
cursor.execute('SELECT name, image FROM team_members')
results = cursor.fetchall()
print('Team members in database:')
for name, image in results:
    print(f'{name}: {image or "No image"}')
conn.close()
