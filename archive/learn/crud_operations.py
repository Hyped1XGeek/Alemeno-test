#!/usr/bin/env python3
"""
PostgreSQL CRUD operations example using psycopg2.
This demonstrates Create, Read, Update, and Delete operations.
"""

from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from psycopg2 import Error


@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='credit_system',
            user='postgres',
            password='Anand123*'
        )
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        yield cursor
    except Error as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


class UserManager:
    """User management class with CRUD operations."""

    def __init__(self):
        self.table_name = 'users'

    def create_table(self):
        """Create the users table if it doesn't exist."""
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                age INTEGER,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        with get_db_connection() as cursor:
            cursor.execute(create_table_query)
            cursor.connection.commit()
            print("✅ Users table created/verified")

    def create_user(self, username, email, full_name, age=None):
        """Create a new user (CREATE operation)."""
        insert_query = """
            INSERT INTO users (username, email, full_name, age)
            VALUES (%s, %s, %s, %s)
            RETURNING id, username, email, full_name, age, is_active, created_at;
        """

        try:
            with get_db_connection() as cursor:
                cursor.execute(insert_query, (username, email, full_name, age))
                result = cursor.fetchone()
                cursor.connection.commit()
                print(f"✅ User created: {result['username']} (ID: {result['id']})")
                return result
        except Error as e:
            print(f"❌ Error creating user: {e}")
            return None

    def read_user(self, user_id):
        """Read a user by ID (READ operation)."""
        select_query = """
            SELECT id, username, email, full_name, age, is_active, created_at, updated_at
            FROM users WHERE id = %s;
        """

        try:
            with get_db_connection() as cursor:
                cursor.execute(select_query, (user_id,))
                result = cursor.fetchone()
                if result:
                    print(f"📖 User found: {result['username']}")
                    return result
                else:
                    print(f"❌ User with ID {user_id} not found")
                    return None
        except Error as e:
            print(f"❌ Error reading user: {e}")
            return None

    def read_all_users(self):
        """Read all users (READ operation)."""
        select_query = """
            SELECT id, username, email, full_name, age, is_active, created_at, updated_at
            FROM users ORDER BY created_at DESC;
        """

        try:
            with get_db_connection() as cursor:
                cursor.execute(select_query)
                results = cursor.fetchall()
                print(f"📖 Found {len(results)} users")
                return results
        except Error as e:
            print(f"❌ Error reading users: {e}")
            return []

    def update_user(self, user_id, **kwargs):
        """Update a user (UPDATE operation)."""
        # Build dynamic update query
        allowed_fields = ['username', 'email', 'full_name', 'age', 'is_active']
        update_fields = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                update_fields.append(f"{field} = %s")
                values.append(value)

        if not update_fields:
            print("❌ No valid fields to update")
            return None

        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(user_id)

        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id, username, email, full_name, age, is_active, created_at, updated_at;
        """

        try:
            with get_db_connection() as cursor:
                cursor.execute(update_query, values)
                result = cursor.fetchone()
                cursor.connection.commit()

                if result:
                    print(f"✅ User updated: {result['username']} (ID: {result['id']})")
                    return result
                else:
                    print(f"❌ User with ID {user_id} not found")
                    return None
        except Error as e:
            print(f"❌ Error updating user: {e}")
            return None

    def delete_user(self, user_id):
        """Delete a user (DELETE operation)."""
        delete_query = """
            DELETE FROM users WHERE id = %s
            RETURNING id, username, email, full_name;
        """

        try:
            with get_db_connection() as cursor:
                cursor.execute(delete_query, (user_id,))
                result = cursor.fetchone()
                cursor.connection.commit()

                if result:
                    print(f"🗑️ User deleted: {result['username']} (ID: {result['id']})")
                    return result
                else:
                    print(f"❌ User with ID {user_id} not found")
                    return None
        except Error as e:
            print(f"❌ Error deleting user: {e}")
            return None

    def search_users(self, search_term):
        """Search users by username, email, or full name."""
        search_query = """
            SELECT id, username, email, full_name, age, is_active, created_at
            FROM users 
            WHERE username ILIKE %s OR email ILIKE %s OR full_name ILIKE %s
            ORDER BY username;
        """

        search_pattern = f"%{search_term}%"

        try:
            with get_db_connection() as cursor:
                cursor.execute(search_query, (search_pattern, search_pattern, search_pattern))
                results = cursor.fetchall()
                print(f"🔍 Found {len(results)} users matching '{search_term}'")
                return results
        except Error as e:
            print(f"❌ Error searching users: {e}")
            return []

    def get_user_stats(self):
        """Get user statistics."""
        stats_query = """
            SELECT 
                COUNT(*) as total_users,
                COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active_users,
                COUNT(CASE WHEN is_active = FALSE THEN 1 END) as inactive_users,
                AVG(age) as average_age,
                MIN(created_at) as first_user_created,
                MAX(created_at) as last_user_created
            FROM users;
        """

        try:
            with get_db_connection() as cursor:
                cursor.execute(stats_query)
                result = cursor.fetchone()
                print("📊 User Statistics:")
                print(f"  Total Users: {result['total_users']}")
                print(f"  Active Users: {result['active_users']}")
                print(f"  Inactive Users: {result['inactive_users']}")
                print(f"  Average Age: {result['average_age']:.1f}" if result['average_age'] else "  Average Age: N/A")
                print(f"  First User Created: {result['first_user_created']}")
                print(f"  Last User Created: {result['last_user_created']}")
                return result
        except Error as e:
            print(f"❌ Error getting user stats: {e}")
            return None


def demo_crud_operations():
    """Demonstrate all CRUD operations."""

    print("🐘 PostgreSQL CRUD Operations Demo")
    print("=" * 60)

    # Initialize user manager
    user_manager = UserManager()

    # Create table
    print("\n🏗️ Setting up database table...")
    user_manager.create_table()

    # CREATE operations
    print("\n📝 CREATE Operations:")
    print("-" * 30)

    users_data = [
        ('john_doe', 'john@example.com', 'John Doe', 25),
        ('jane_smith', 'jane@example.com', 'Jane Smith', 30),
        ('bob_wilson', 'bob@example.com', 'Bob Wilson', 35),
        ('alice_brown', 'alice@example.com', 'Alice Brown', 28),
        ('charlie_davis', 'charlie@example.com', 'Charlie Davis', 32)
    ]

    created_users = []
    for username, email, full_name, age in users_data:
        user = user_manager.create_user(username, email, full_name, age)
        if user:
            created_users.append(user)

    # READ operations
    print("\n📖 READ Operations:")
    print("-" * 30)

    # Read all users
    all_users = user_manager.read_all_users()
    print(f"All users ({len(all_users)}):")
    for user in all_users:
        print(f"  ID: {user['id']}, Username: {user['username']}, Email: {user['email']}, Age: {user['age']}")

    # Read specific user
    if created_users:
        first_user = user_manager.read_user(created_users[0]['id'])
        if first_user:
            print("\nSpecific user details:")
            print(f"  Username: {first_user['username']}")
            print(f"  Email: {first_user['email']}")
            print(f"  Full Name: {first_user['full_name']}")
            print(f"  Age: {first_user['age']}")
            print(f"  Active: {first_user['is_active']}")
            print(f"  Created: {first_user['created_at']}")

    # UPDATE operations
    print("\n✏️ UPDATE Operations:")
    print("-" * 30)

    if created_users:
        # Update first user's age and status
        updated_user = user_manager.update_user(
            created_users[0]['id'],
            age=26,
            is_active=False
        )

        if updated_user:
            print(f"Updated user: {updated_user['username']}, Age: {updated_user['age']}, Active: {updated_user['is_active']}")

    # SEARCH operations
    print("\n🔍 SEARCH Operations:")
    print("-" * 30)

    # Search for users with 'john' in their data
    search_results = user_manager.search_users('john')
    for user in search_results:
        print(f"  Found: {user['username']} ({user['email']})")

    # STATISTICS
    print("\n📊 STATISTICS:")
    print("-" * 30)
    user_manager.get_user_stats()

    # DELETE operations
    print("\n🗑️ DELETE Operations:")
    print("-" * 30)

    if len(created_users) > 1:
        # Delete the last created user
        deleted_user = user_manager.delete_user(created_users[-1]['id'])
        if deleted_user:
            print(f"Deleted user: {deleted_user['username']}")

    # Final statistics
    print("\n📊 Final Statistics:")
    print("-" * 30)
    user_manager.get_user_stats()

    print("\n✅ CRUD operations demo completed!")


def demo_batch_operations():
    """Demonstrate batch operations."""

    print("\n🔄 Batch Operations Demo")
    print("-" * 40)

    user_manager = UserManager()
    user_manager.create_table()

    # Batch insert
    print("📝 Batch Insert:")
    batch_data = [
        ('batch_user1', 'batch1@example.com', 'Batch User 1', 25),
        ('batch_user2', 'batch2@example.com', 'Batch User 2', 30),
        ('batch_user3', 'batch3@example.com', 'Batch User 3', 35)
    ]

    insert_query = """
        INSERT INTO users (username, email, full_name, age)
        VALUES (%s, %s, %s, %s)
        RETURNING id, username;
    """

    try:
        with get_db_connection() as cursor:
            cursor.executemany(insert_query, batch_data)
            results = cursor.fetchall()
            cursor.connection.commit()
            print(f"✅ Batch inserted {len(results)} users")
            for result in results:
                print(f"  - {result['username']} (ID: {result['id']})")
    except Error as e:
        print(f"❌ Error in batch insert: {e}")

    # Batch update
    print("\n✏️ Batch Update:")
    update_query = """
        UPDATE users 
        SET is_active = %s, updated_at = CURRENT_TIMESTAMP
        WHERE username LIKE %s
        RETURNING username, is_active;
    """

    try:
        with get_db_connection() as cursor:
            cursor.execute(update_query, (False, 'batch_%'))
            results = cursor.fetchall()
            cursor.connection.commit()
            print(f"✅ Batch updated {len(results)} users")
            for result in results:
                print(f"  - {result['username']}: Active = {result['is_active']}")
    except Error as e:
        print(f"❌ Error in batch update: {e}")


def main():
    """Main function to run CRUD demos."""

    try:
        demo_crud_operations()
        demo_batch_operations()

        print("\n🏁 All CRUD demos completed successfully!")

    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
