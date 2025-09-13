#!/usr/bin/env python3
"""
Database setup script to create the credit_system database.
This script connects to the default 'postgres' database and creates the required database.
"""

import psycopg2
import psycopg2.extensions
from psycopg2 import Error


def create_database():
    """Create the credit_system database if it doesn't exist."""

    # Connect to default 'postgres' database
    connection_params = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',  # Connect to default database
        'user': 'postgres',
        'password': 'Anand123*'
    }

    connection = None
    cursor = None

    try:
        print("🐘 Connecting to PostgreSQL server...")
        print(f"Host: {connection_params['host']}:{connection_params['port']}")
        print(f"Database: {connection_params['database']}")
        print(f"User: {connection_params['user']}")
        print("-" * 50)

        # Create connection to default database
        connection = psycopg2.connect(**connection_params)
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        print("✅ Connected to PostgreSQL server!")

        # Check if credit_system database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'credit_system';")
        exists = cursor.fetchone()

        if exists:
            print("✅ Database 'credit_system' already exists!")
        else:
            print("🏗️ Creating database 'credit_system'...")
            cursor.execute('CREATE DATABASE credit_system;')
            print("✅ Database 'credit_system' created successfully!")

        # List all databases
        print("\n📋 Available databases:")
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;")
        databases = cursor.fetchall()
        for db in databases:
            print(f"  - {db[0]}")

        return True

    except (Exception, Error) as error:
        print(f"❌ Error: {error}")
        return False

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("🔌 Connection closed")


def test_credit_system_connection():
    """Test connection to the credit_system database."""

    connection_params = {
        'host': 'localhost',
        'port': '5432',
        'database': 'credit_system',
        'user': 'postgres',
        'password': 'Anand123*'
    }

    connection = None
    cursor = None

    try:
        print("\n🧪 Testing connection to credit_system database...")
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Test basic query
        cursor.execute("SELECT current_database(), version();")
        result = cursor.fetchone()

        print("✅ Successfully connected to credit_system database!")
        print(f"Database: {result[0]}")
        print(f"Version: {result[1][:50]}...")

        return True

    except (Exception, Error) as error:
        print(f"❌ Error connecting to credit_system: {error}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    """Main function to set up the database."""

    print("🐘 PostgreSQL Database Setup")
    print("=" * 50)

    # Create the database
    if create_database():
        # Test the connection
        test_credit_system_connection()
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the connection examples in the learn/ directory.")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your Docker container and try again.")


if __name__ == "__main__":
    main()
