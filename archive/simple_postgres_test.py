#!/usr/bin/env python3
"""
Simple PostgreSQL connection test.
Minimal example to verify database connectivity.
"""


import psycopg2


def main():
    """Simple connection test to PostgreSQL database."""

    # Database connection parameters
    # These match your Docker setup
    db_config = {
        'host': 'localhost',        # Your Docker PostgreSQL host
        'port': '5432',            # PostgreSQL port
        'database': 'credit_system', # Database name
        'user': 'postgres',        # Username
        'password': 'Anand123*',    # Password
    }

    print("🐘 Testing PostgreSQL Connection")
    print("-" * 40)
    print(f"Host: {db_config['host']}:{db_config['port']}")
    print(f"Database: {db_config['database']}")
    print(f"User: {db_config['user']}")
    print()

    try:
        # Attempt to connect
        print("Connecting...")
        connection = psycopg2.connect(**db_config)

        # Create cursor
        cursor = connection.cursor()

        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print("✅ Connection successful!")
        print(f"PostgreSQL Version: {version[0]}")

        # Close connection
        cursor.close()
        connection.close()
        print("🔌 Connection closed")

    except psycopg2.Error as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Docker container is running")
        print("2. Check if port 5432 is accessible")
        print("3. Verify database credentials")
        print("4. Try: docker ps (to see running containers)")


if __name__ == "__main__":
    main()
