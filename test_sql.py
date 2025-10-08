#!/usr/bin/env python3
"""
Example script showing how to properly execute SQL queries in Python
"""

import sqlite3
import os

def test_database_connection():
    """Test database connection and run a simple query"""
    
    # Path to the database (adjust as needed)
    db_path = "../michelleweon-hw4/data.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Example 1: Count total records
        cursor.execute("SELECT COUNT(*) as total FROM zip_county")
        result = cursor.fetchone()
        print(f"Total zip_county records: {result[0]}")
        
        # Example 2: Get some sample data
        cursor.execute("""
            SELECT county, state_abbreviation, COUNT(*) as zip_count 
            FROM zip_county 
            WHERE state_abbreviation = 'CA' 
            GROUP BY county, state_abbreviation 
            ORDER BY zip_count DESC 
            LIMIT 5
        """)
        
        print("\nTop 5 counties in California by ZIP count:")
        for row in cursor.fetchall():
            print(f"  {row['county']}, {row['state_abbreviation']}: {row['zip_count']} ZIP codes")
        
        # Example 3: Parameterized query (secure way)
        state = 'TX'
        cursor.execute("SELECT COUNT(*) FROM zip_county WHERE state_abbreviation = ?", (state,))
        tx_count = cursor.fetchone()[0]
        print(f"\nTotal ZIP codes in Texas: {tx_count}")
        
        # Close the connection
        conn.close()
        print("\nDatabase connection closed successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_database_connection()
