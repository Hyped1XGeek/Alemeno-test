#!/usr/bin/env python3
"""
Startup script for the Credit Approval System.

This script sets up the database, imports data, and starts the Django server.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=project_root, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import django
        import rest_framework
        import pandas
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: uv sync")
        return False


def setup_database():
    """Set up the database."""
    commands = [
        ("uv run python manage.py makemigrations", "Creating migrations"),
        ("uv run python manage.py migrate", "Applying migrations"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True


def import_data():
    """Import sample data."""
    return run_command(
        "uv run python manage.py import_data", 
        "Importing customer and loan data"
    )


def create_superuser():
    """Create a superuser if it doesn't exist."""
    print("🔍 Checking for superuser...")
    
    try:
        # Try to import Django and check for superuser
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        import django
        django.setup()
        
        from django.contrib.auth.models import User
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            return True
        else:
            print("👤 Creating superuser...")
            print("Please enter superuser details:")
            return run_command(
                "uv run python manage.py createsuperuser", 
                "Creating superuser"
            )
    except Exception as e:
        print(f"⚠️ Could not check superuser: {e}")
        return True


def start_server():
    """Start the Django development server."""
    print("🚀 Starting Django development server...")
    print("Server will be available at: http://localhost:8000")
    print("API endpoints: http://localhost:8000/api/")
    print("Admin interface: http://localhost:8000/admin/")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run(
            "uv run python manage.py runserver", 
            shell=True, 
            cwd=project_root, 
            check=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")


def main():
    """Main startup function."""
    print("=" * 60)
    print("🏦 Credit Approval System - Startup Script")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        sys.exit(1)
    
    # Import data
    if not import_data():
        print("⚠️ Data import failed, but continuing...")
    
    # Create superuser
    if not create_superuser():
        print("⚠️ Superuser creation failed, but continuing...")
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
