import pandas as pd
import sqlite3

# Connect to the SQLite database (assumes it's in the current directory)
conn = sqlite3.connect('shipping.db')
cursor = conn.cursor()

# Create the table if it doesn't exist (adjust schema as per actual DB)
cursor.execute('''
CREATE TABLE IF NOT EXISTS shipments (
    shipping_id INTEGER,
    product TEXT,
    quantity INTEGER,
    origin TEXT,
    destination TEXT
)
''')
conn.commit()

# Part 1: Insert Spreadsheet 0 (self-contained)
print("Inserting data from Spreadsheet 0...")
df0 = pd.read_csv('spreadsheet0.csv')
# Assume columns match: shipping_id, product, quantity, origin, destination
df0.to_sql('shipments', conn, if_exists='append', index=False)
print(f"Inserted {len(df0)} rows from Spreadsheet 0.")

# Part 2: Handle Spreadsheets 1 and 2 (dependent)
print("Processing Spreadsheets 1 and 2...")
df1 = pd.read_csv('spreadsheet1.csv')  # Columns: shipping_id, product, quantity
df2 = pd.read_csv('spreadsheet2.csv')  # Columns: shipping_id, origin, destination

# Merge on shipping_id to combine shipment details with products
df_combined = df1.merge(df2, on='shipping_id', how='inner')

# Optional: If total shipment quantity is needed, group and sum quantities per shipment
# But since we insert per product, we'll use per-product quantity
# Example: shipment_quantities = df1.groupby('shipping_id')['quantity'].sum().to_dict()
# Then add to df_combined if required (e.g., df_combined['total_shipment_qty'] = df_combined['shipping_id'].map(shipment_quantities))

# Insert the combined data (one row per product)
df_combined.to_sql('shipments', conn, if_exists='append', index=False)
print(f"Inserted {len(df_combined)} rows from combined Spreadsheets 1 and 2.")

# Close the connection
conn.close()
print("Database population complete!")