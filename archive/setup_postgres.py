#!/usr/bin/env python3
"""
Setup script for PostgreSQL database.

This script helps set up the PostgreSQL database for the Credit Approval System.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def run_command(command, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def create_database():
    """Create the PostgreSQL database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        db_name = os.getenv("DB_NAME", "credit_system")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        
        if cursor.fetchone():
            print(f"✅ Database '{db_name}' already exists")
        else:
            # Create database
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database '{db_name}' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def setup_postgres():
    """Main setup function."""
    print("🚀 Setting up PostgreSQL for Credit Approval System")
    print("=" * 50)
    
    # Check if PostgreSQL is running
    if not run_command("pg_isready", "Checking PostgreSQL connection"):
        print("❌ PostgreSQL is not running. Please start PostgreSQL first.")
        print("💡 On Windows: Start PostgreSQL service")
        print("💡 On macOS: brew services start postgresql")
        print("💡 On Linux: sudo systemctl start postgresql")
        return False
    
    # Create database
    if not create_database():
        return False
    
    # Install dependencies
    if not run_command("uv sync", "Installing dependencies"):
        return False
    
    # Run migrations
    if not run_command("uv run python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("uv run python manage.py migrate", "Applying migrations"):
        return False
    
    # Import data
    if not run_command("uv run python manage.py import_data", "Importing sample data"):
        return False
    
    print("\n" + "=" * 50)
    print("🎉 PostgreSQL setup completed successfully!")
    print("💡 You can now run: uv run python manage.py runserver")
    return True

if __name__ == "__main__":
    setup_postgres()
