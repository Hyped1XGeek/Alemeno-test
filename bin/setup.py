#!/usr/bin/env python3
"""
Setup script for the Credit Approval System.

This script installs dependencies and sets up the project.
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
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 13:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("Please use Python 3.13 or higher")
        return False


def install_uv():
    """Install uv package manager."""
    print("📦 Checking for uv package manager...")
    try:
        result = subprocess.run(
            "uv --version", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print(f"✅ uv is already installed: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("📦 Installing uv...")
    return run_command(
        "pip install uv", 
        "Installing uv package manager"
    )


def install_dependencies():
    """Install project dependencies."""
    return run_command(
        "uv sync", 
        "Installing project dependencies"
    )


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


def run_tests():
    """Run system tests."""
    return run_command(
        "uv run python bin/test_system.py", 
        "Running system tests"
    )


def main():
    """Main setup function."""
    print("=" * 60)
    print("🏦 Credit Approval System - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install uv
    if not install_uv():
        print("❌ Failed to install uv")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        sys.exit(1)
    
    # Import data
    if not import_data():
        print("⚠️ Data import failed, but continuing...")
    
    # Run tests
    if not run_tests():
        print("⚠️ Tests failed, but continuing...")
    
    print("=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("Next steps:")
    print("1. Run: python bin/start_server.py")
    print("2. Visit: http://localhost:8000/api/")
    print("3. Admin: http://localhost:8000/admin/")
    print("=" * 60)


if __name__ == "__main__":
    main()
