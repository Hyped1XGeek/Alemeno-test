#!/usr/bin/env python3
"""
Basic PostgreSQL connection example using psycopg2.
This is the simplest way to connect to your PostgreSQL database.
"""

import psycopg2
from psycopg2 import Error


def basic_connection():
    """Basic connection to PostgreSQL database."""

    # Database connection parameters
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
        print("🐘 Connecting to PostgreSQL database...")
        print(f"Host: {connection_params['host']}:{connection_params['port']}")
        print(f"Database: {connection_params['database']}")
        print(f"User: {connection_params['user']}")
        print("-" * 50)

        # Create connection
        connection = psycopg2.connect(**connection_params)

        # Create cursor
        cursor = connection.cursor()

        # Test the connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print("✅ Connection successful!")
        print(f"PostgreSQL Version: {version[0]}")

        # Get current time
        cursor.execute("SELECT NOW();")
        current_time = cursor.fetchone()
        print(f"Current Database Time: {current_time[0]}")

        return True

    except (Exception, Error) as error:
        print(f"❌ Error connecting to PostgreSQL: {error}")
        return False

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("🔌 Connection closed")


if __name__ == "__main__":
    print("PostgreSQL Basic Connection Test")
    print("=" * 50)
    basic_connection()
