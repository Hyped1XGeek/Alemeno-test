#!/usr/bin/env python3
"""
Sample program to test PostgreSQL connection to the Docker database.
This script demonstrates how to connect to the PostgreSQL database running in Docker.
"""

import psycopg2
import psycopg2.extras
from psycopg2 import sql
import os
import sys
from datetime import datetime


def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    Uses the same configuration as your Django settings.
    """
    try:
        # Database connection parameters
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'credit_system'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'Anand123*'),
        }
        
        print("Attempting to connect to PostgreSQL database...")
        print(f"Host: {db_config['host']}")
        print(f"Port: {db_config['port']}")
        print(f"Database: {db_config['database']}")
        print(f"User: {db_config['user']}")
        print("-" * 50)
        
        # Create connection
        connection = psycopg2.connect(**db_config)
        return connection   
        
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def test_connection():
    """
    Test the database connection and perform basic operations.
    """
    connection = get_db_connection()
    
    if connection is None:
        print("❌ Failed to connect to database")
        return False
    
    try:
        # Create a cursor
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        print("✅ Successfully connected to PostgreSQL database!")
        print()
        
        # Test 1: Get database version
        print("📊 Database Information:")
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL Version: {version['version']}")
        print()
        
        # Test 2: List all databases
        print("🗄️ Available Databases:")
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        for db in databases:
            print(f"  - {db['datname']}")
        print()
        
        # Test 3: List tables in current database
        print("📋 Tables in current database:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  No tables found in the public schema")
        print()
        
        # Test 4: Get current timestamp
        print("⏰ Current Database Time:")
        cursor.execute("SELECT NOW() as current_time;")
        current_time = cursor.fetchone()
        print(f"Database Time: {current_time['current_time']}")
        print()
        
        # Test 5: Test a simple query
        print("🧪 Testing a simple query:")
        cursor.execute("SELECT 1 + 1 as result, 'Hello PostgreSQL!' as message;")
        result = cursor.fetchone()
        print(f"Result: {result['result']}")
        print(f"Message: {result['message']}")
        print()
        
        print("✅ All tests passed successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
        
    finally:
        if connection:
            connection.close()
            print("🔌 Database connection closed")


def create_sample_table():
    """
    Create a sample table to demonstrate database operations.
    """
    connection = get_db_connection()
    
    if connection is None:
        print("❌ Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create a sample table
        print("🏗️ Creating sample table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sample_data (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insert some sample data
        print("📝 Inserting sample data...")
        sample_data = [
            ('John Doe', 'john.doe@example.com'),
            ('Jane Smith', 'jane.smith@example.com'),
            ('Bob Johnson', 'bob.johnson@example.com'),
        ]
        
        for name, email in sample_data:
            cursor.execute("""
                INSERT INTO sample_data (name, email) 
                VALUES (%s, %s) 
                ON CONFLICT (email) DO NOTHING;
            """, (name, email))
        
        # Query the data
        print("📊 Sample data in table:")
        cursor.execute("SELECT * FROM sample_data ORDER BY id;")
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Created: {row[3]}")
        
        # Commit the transaction
        connection.commit()
        print("✅ Sample table created and populated successfully!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating sample table: {e}")
        connection.rollback()
        return False
        
    finally:
        if connection:
            connection.close()


def main():
    """
    Main function to run the PostgreSQL connection tests.
    """
    print("🐘 PostgreSQL Connection Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    print()
    
    # Test basic connection
    if test_connection():
        print()
        print("🎯 Would you like to create a sample table? (y/n): ", end="")
        
        # For automated testing, we'll skip the interactive part
        # In a real scenario, you could use: response = input()
        response = "y"  # Auto-approve for demo
        
        if response.lower() in ['y', 'yes']:
            print()
            create_sample_table()
    
    print()
    print("=" * 50)
    print("🏁 Test completed!")


if __name__ == "__main__":
    main()
