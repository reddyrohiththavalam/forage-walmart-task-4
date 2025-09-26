"""
Python Script to Populate Walmart SQLite Database from Spreadsheets

Instructions:
1. Place the spreadsheet files in the same directory as this script.
2. Ensure pandas and sqlite3 libraries are installed.
3. Run the script to populate the database.
"""

import sqlite3
import pandas as pd

# Step 1: Load the spreadsheets
spreadsheet_0 = pd.read_excel("spreadsheet0.xlsx")
spreadsheet_1 = pd.read_excel("spreadsheet1.xlsx")
spreadsheet_2 = pd.read_excel("spreadsheet2.xlsx")

# Step 2: Connect to the SQLite database
conn = sqlite3.connect("walmart.db")
cursor = conn.cursor()

# Optional: Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    origin TEXT,
    destination TEXT,
    PRIMARY KEY (shipment_id, product_id)
)
''')

# Step 3: Populate spreadsheet 0 data (self-contained)
for _, row in spreadsheet_0.iterrows():
    cursor.execute('''
    INSERT INTO products (product_name, category, price)
    VALUES (?, ?, ?)
    ''', (row['product_name'], row['category'], row['price']))

# Step 4: Merge spreadsheet 1 and 2 for shipment data
shipments_merged = pd.merge(spreadsheet_1, spreadsheet_2, on='shipment_id', how='left')

for _, row in shipments_merged.iterrows():
    cursor.execute('''
    INSERT INTO shipments (shipment_id, product_id, quantity, origin, destination)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['shipment_id'], row['product_id'], row['quantity'], row['origin'], row['destination']))

# Step 5: Commit changes and close connection
conn.commit()
conn.close()

print("Database populated successfully!")

