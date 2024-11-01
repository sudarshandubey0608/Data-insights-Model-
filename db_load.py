import sqlite3

# Path to your SQLite database
db_path = '/home/sam/Documents/Data Insights/nba.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to display all tables and their columns
def get_db_schema(cursor):
    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Database Schema:")
    for table in tables:
        print(f"\nTable: {table[0]}")
        # Query to get the columns for the current table
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"Column: {col[1]} | Type: {col[2]}")

# Call the function to display the schema
get_db_schema(cursor)

# Close the connection
conn.close()
