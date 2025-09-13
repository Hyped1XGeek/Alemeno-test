#!/usr/bin/env python3
"""
Advanced PostgreSQL connection example with comprehensive error handling.
This example shows how to handle various connection scenarios and errors.
"""

import sys
import time

import psycopg2
import psycopg2.extras
from psycopg2 import DatabaseError, Error, OperationalError


class PostgreSQLConnection:
    """Advanced PostgreSQL connection class with error handling."""

    def __init__(self, host='localhost', port='5432', database='credit_system',
                 user='postgres', password='Anand123*'):
        self.connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.connection = None
        self.cursor = None

    def connect(self, max_retries=3, retry_delay=2):
        """Connect to PostgreSQL with retry logic."""

        for attempt in range(max_retries):
            try:
                print(f"🔄 Connection attempt {attempt + 1}/{max_retries}")
                print(f"Host: {self.connection_params['host']}:{self.connection_params['port']}")
                print(f"Database: {self.connection_params['database']}")
                print(f"User: {self.connection_params['user']}")
                print("-" * 50)

                # Create connection with timeout
                self.connection = psycopg2.connect(
                    **self.connection_params,
                    connect_timeout=10
                )

                # Set autocommit to False for transaction control
                self.connection.autocommit = False

                # Create cursor with dictionary-like access
                self.cursor = self.connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

                print("✅ Connection successful!")
                return True

            except OperationalError as e:
                print(f"❌ Operational Error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print(f"⏳ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("💥 Max retries reached. Connection failed.")
                    return False

            except DatabaseError as e:
                print(f"❌ Database Error: {e}")
                return False

            except Error as e:
                print(f"❌ PostgreSQL Error: {e}")
                return False

            except Exception as e:
                print(f"❌ Unexpected Error: {e}")
                return False

    def test_connection(self):
        """Test the database connection with various queries."""

        if not self.connection or not self.cursor:
            print("❌ No active connection")
            return False

        try:
            print("\n🧪 Testing database connection...")

            # Test 1: Get PostgreSQL version
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()
            print(f"📊 PostgreSQL Version: {version['version']}")

            # Test 2: Get current database info
            self.cursor.execute("SELECT current_database(), current_user, inet_server_addr();")
            db_info = self.cursor.fetchone()
            print(f"🗄️ Current Database: {db_info['current_database']}")
            print(f"👤 Current User: {db_info['current_user']}")
            print(f"🌐 Server Address: {db_info['inet_server_addr']}")

            # Test 3: Get current timestamp
            self.cursor.execute("SELECT NOW() as current_time, timezone('UTC', NOW()) as utc_time;")
            time_info = self.cursor.fetchone()
            print(f"⏰ Local Time: {time_info['current_time']}")
            print(f"🌍 UTC Time: {time_info['utc_time']}")

            # Test 4: List databases
            self.cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;")
            databases = self.cursor.fetchall()
            print(f"📋 Available Databases ({len(databases)}):")
            for db in databases:
                print(f"  - {db['datname']}")

            # Test 5: List tables in current database
            self.cursor.execute("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            tables = self.cursor.fetchall()
            print(f"\n📋 Tables in current database ({len(tables)}):")
            if tables:
                for table in tables:
                    print(f"  - {table['table_name']} ({table['table_type']})")
            else:
                print("  No tables found in public schema")

            print("\n✅ All connection tests passed!")
            return True

        except Error as e:
            print(f"❌ Error during connection test: {e}")
            return False

    def execute_query(self, query, params=None):
        """Execute a query and return results."""

        if not self.connection or not self.cursor:
            print("❌ No active connection")
            return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Check if query returns data
            if self.cursor.description:
                results = self.cursor.fetchall()
                return results
            else:
                return f"Query executed successfully. Rows affected: {self.cursor.rowcount}"

        except Error as e:
            print(f"❌ Error executing query: {e}")
            return None

    def commit(self):
        """Commit the current transaction."""
        if self.connection:
            self.connection.commit()
            print("✅ Transaction committed")

    def rollback(self):
        """Rollback the current transaction."""
        if self.connection:
            self.connection.rollback()
            print("🔄 Transaction rolled back")

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("🔌 Connection closed")


def main():
    """Main function to demonstrate advanced connection."""

    print("🐘 Advanced PostgreSQL Connection Test")
    print("=" * 60)

    # Create connection instance
    db = PostgreSQLConnection()

    try:
        # Attempt to connect
        if db.connect():
            # Test the connection
            if db.test_connection():
                print("\n🎯 Connection is working perfectly!")

                # Example: Execute a custom query
                print("\n🔍 Example: Getting database size")
                result = db.execute_query("""
                    SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;
                """)
                if result:
                    print(f"Database Size: {result[0]['db_size']}")

            # Commit any pending transactions
            db.commit()

        else:
            print("❌ Failed to establish connection")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        db.rollback()

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        db.rollback()

    finally:
        # Always close the connection
        db.close()
        print("\n🏁 Test completed!")


if __name__ == "__main__":
    main()
