#!/usr/bin/env python3
"""
Complete PostgreSQL Docker setup script for Credit Approval System.
This script sets up the database, runs migrations, and imports data.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2 import Error
import psycopg2.extensions


def check_docker_postgres():
    """Check if Docker PostgreSQL container is running."""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if 'postgres' in result.stdout.lower():
            print("✅ Docker PostgreSQL container is running")
            return True
        else:
            print("❌ Docker PostgreSQL container is not running")
            print("Please run: docker-compose up -d db")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed or not in PATH")
        return False


def create_database():
    """Create the credit_system database if it doesn't exist."""
    
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


def test_connection():
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


def run_django_commands():
    """Run Django management commands."""
    
    # Set environment variables
    os.environ['DB_PASSWORD'] = 'Anand123*'
    os.environ['DB_NAME'] = 'credit_system'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    
    commands = [
        ['uv', 'run', 'python', 'manage.py', 'migrate'],
        ['uv', 'run', 'python', 'manage.py', 'import_data'],
    ]
    
    for cmd in commands:
        print(f"\n🔄 Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Command completed successfully")
            if result.stdout:
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False
    
    return True


def test_api():
    """Test the API endpoints."""
    import requests
    import time
    
    print("\n🧪 Testing API endpoints...")
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        # Test stats endpoint
        response = requests.get('http://127.0.0.1:8000/api/stats/', timeout=5)
        if response.status_code == 200:
            print("✅ API is responding correctly")
            data = response.json()
            print(f"Total customers: {data.get('total_customers', 'N/A')}")
            print(f"Total loans: {data.get('total_loans', 'N/A')}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API test failed: {e}")
        return False


def main():
    """Main setup function."""
    
    print("🐘 Credit Approval System - PostgreSQL Docker Setup")
    print("=" * 60)
    
    # Step 1: Check Docker PostgreSQL
    if not check_docker_postgres():
        print("\n❌ Please start Docker PostgreSQL first:")
        print("   docker-compose up -d db")
        return False
    
    # Step 2: Create database
    if not create_database():
        print("\n❌ Database creation failed!")
        return False
    
    # Step 3: Test connection
    if not test_connection():
        print("\n❌ Connection test failed!")
        return False
    
    # Step 4: Run Django commands
    if not run_django_commands():
        print("\n❌ Django setup failed!")
        return False
    
    print("\n🎉 PostgreSQL Docker setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the Django server: uv run python manage.py runserver")
    print("2. Test the API: uv run python bin/test_all_endpoints.py")
    print("3. Access the admin: http://127.0.0.1:8000/admin/")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
