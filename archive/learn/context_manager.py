#!/usr/bin/env python3
"""
PostgreSQL connection using context manager for automatic resource management.
This is the recommended way to handle database connections in Python.
"""

from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from psycopg2 import Error


class DatabaseConnection:
    """PostgreSQL connection class with context manager support."""

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

    def __enter__(self):
        """Enter the context manager."""
        try:
            print("🔌 Opening database connection...")
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            print("✅ Connection established")
            return self
        except Error as e:
            print(f"❌ Failed to connect: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        try:
            if exc_type is not None:
                # An exception occurred, rollback the transaction
                print("🔄 Exception occurred, rolling back transaction...")
                if self.connection:
                    self.connection.rollback()
            else:
                # No exception, commit the transaction
                print("✅ Committing transaction...")
                if self.connection:
                    self.connection.commit()
        except Error as e:
            print(f"❌ Error during cleanup: {e}")
        finally:
            # Always close the connection
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("🔌 Connection closed")

    def execute(self, query, params=None):
        """Execute a query."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        if self.cursor.description:
            return self.cursor.fetchall()
        return f"Query executed. Rows affected: {self.cursor.rowcount}"

    def execute_many(self, query, params_list):
        """Execute a query multiple times with different parameters."""
        self.cursor.executemany(query, params_list)
        return f"Batch executed. Rows affected: {self.cursor.rowcount}"


@contextmanager
def get_db_connection(host='localhost', port='5432', database='credit_system',
                     user='postgres', password='Anand123*'):
    """
    Context manager function for database connections.
    This is an alternative to the class-based approach.
    """
    connection = None
    cursor = None

    try:
        print("🔌 Opening database connection...")
        connection = psycopg2.connect(
            host=host, port=port, database=database,
            user=user, password=password
        )
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        print("✅ Connection established")
        yield cursor

    except Error as e:
        print(f"❌ Database error: {e}")
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("🔌 Connection closed")


def demo_class_context_manager():
    """Demonstrate class-based context manager."""

    print("🏗️ Class-based Context Manager Demo")
    print("-" * 50)

    try:
        with DatabaseConnection() as db:
            # Test basic connection
            result = db.execute("SELECT version();")
            print(f"PostgreSQL Version: {result[0]['version']}")

            # Test current time
            result = db.execute("SELECT NOW() as current_time;")
            print(f"Current Time: {result[0]['current_time']}")

            # Test database info
            result = db.execute("""
                SELECT current_database() as db_name, 
                       current_user as user_name,
                       inet_server_addr() as server_addr;
            """)
            info = result[0]
            print(f"Database: {info['db_name']}")
            print(f"User: {info['user_name']}")
            print(f"Server: {info['server_addr']}")

            print("✅ All operations completed successfully!")

    except Error as e:
        print(f"❌ Error in class context manager: {e}")


def demo_function_context_manager():
    """Demonstrate function-based context manager."""

    print("\n🔧 Function-based Context Manager Demo")
    print("-" * 50)

    try:
        with get_db_connection() as cursor:
            # Test basic connection
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            print(f"PostgreSQL Version: {result['version']}")

            # Test current time
            cursor.execute("SELECT NOW() as current_time;")
            result = cursor.fetchone()
            print(f"Current Time: {result['current_time']}")

            # Test database info
            cursor.execute("""
                SELECT current_database() as db_name, 
                       current_user as user_name,
                       inet_server_addr() as server_addr;
            """)
            result = cursor.fetchone()
            print(f"Database: {result['db_name']}")
            print(f"User: {result['user_name']}")
            print(f"Server: {result['server_addr']}")

            print("✅ All operations completed successfully!")

    except Error as e:
        print(f"❌ Error in function context manager: {e}")


def demo_transaction_handling():
    """Demonstrate transaction handling with context manager."""

    print("\n💳 Transaction Handling Demo")
    print("-" * 50)

    try:
        with DatabaseConnection() as db:
            # Create a test table
            db.execute("""
                CREATE TABLE IF NOT EXISTS test_transactions (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    amount DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Insert some test data
            test_data = [
                ('Transaction 1', 100.50),
                ('Transaction 2', 250.75),
                ('Transaction 3', 75.25)
            ]

            insert_query = """
                INSERT INTO test_transactions (name, amount) 
                VALUES (%s, %s);
            """

            for name, amount in test_data:
                db.execute(insert_query, (name, amount))

            # Query the data
            result = db.execute("SELECT * FROM test_transactions ORDER BY id;")
            print("📊 Test transactions:")
            for row in result:
                print(f"  ID: {row['id']}, Name: {row['name']}, Amount: {row['amount']}, Created: {row['created_at']}")

            # Calculate total
            result = db.execute("SELECT SUM(amount) as total FROM test_transactions;")
            total = result[0]['total']
            print(f"💰 Total Amount: {total}")

            print("✅ Transaction completed successfully!")

    except Error as e:
        print(f"❌ Error in transaction demo: {e}")


def demo_error_handling():
    """Demonstrate error handling with context manager."""

    print("\n⚠️ Error Handling Demo")
    print("-" * 50)

    try:
        with DatabaseConnection() as db:
            # This will cause an error (table doesn't exist)
            print("Attempting to query non-existent table...")
            db.execute("SELECT * FROM non_existent_table;")

    except Error as e:
        print(f"❌ Expected error caught: {e}")
        print("✅ Error handling works correctly!")


def main():
    """Main function to run all context manager demos."""

    print("🐘 PostgreSQL Context Manager Examples")
    print("=" * 60)

    # Run all demos
    demo_class_context_manager()
    demo_function_context_manager()
    demo_transaction_handling()
    demo_error_handling()

    print("\n🏁 All context manager demos completed!")


if __name__ == "__main__":
    main()
