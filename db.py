import sqlite3

# This is the command in question. It goes right after the import.
# It establishes the connection to the database file.
conn = sqlite3.connect('database.db')

# You then use the 'conn' object to get a 'cursor'.
# A cursor is what you use to send commands to the database.
cursor = conn.cursor()

# Define the SQL command to create your table
create_table_query = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    in_stock BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Use the cursor to execute the command
cursor.execute(create_table_query)

# Save (commit) the changes to the database file
conn.commit()

# Always close the connection when you're done
conn.close()

print("Database and 'products' table created successfully.")