#!/usr/bin/env python3
"""
Credit Approval System - Main Application Launcher

This is the main entry point for the Credit Approval System.
It provides options to start the server, run tests, or setup the system.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Initialize logging
try:
    from credit_system.logging_config import setup_logging
    setup_logging()
except ImportError:
    # Fallback if logging config is not available
    import logging
    logging.basicConfig(level=logging.INFO)


def print_banner():
    """Print the application banner."""
    print("=" * 60)
    print("🏦 CREDIT APPROVAL SYSTEM")
    print("=" * 60)
    print("A Django-based credit scoring and loan approval system")
    print("Built with PostgreSQL, Django REST Framework, and Docker")
    print("=" * 60)


def check_requirements():
    """Check if required tools are available."""
    print("🔍 Checking requirements...")
    
    # Check if uv is available
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        print("✅ uv package manager is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv package manager not found. Please install uv first.")
        return False
    
    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✅ Docker is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Docker not found. PostgreSQL will use local installation.")
    
    return True


def setup_system():
    """Setup the system (database, migrations, data import)."""
    print("\n🏗️  Setting up Credit Approval System...")
    
    try:
        # Run the setup script
        result = subprocess.run([
            "uv", "run", "python", "bin/setup_postgres_docker.py"
        ], check=True)
        
        if result.returncode == 0:
            print("✅ System setup completed successfully!")
            return True
        else:
            print("❌ System setup failed!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False


def start_server():
    """Start the Django development server."""
    print("\n🚀 Starting Credit Approval System server...")
    print("📡 Server will be available at: http://127.0.0.1:8000")
    print("🔧 Admin interface: http://127.0.0.1:8000/admin/")
    print("📋 API endpoints: http://127.0.0.1:8000/api/")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        subprocess.run([
            "uv", "run", "python", "manage.py", "runserver"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")


def run_tests():
    """Run the comprehensive tests."""
    print("\n🧪 Running Credit Approval System tests...")
    
    try:
        result = subprocess.run([
            "uv", "run", "python", "bin/run_tests.py", "--all"
        ], check=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Test execution failed: {e}")


def run_unit_tests():
    """Run unit tests only."""
    print("\n🧪 Running unit tests...")
    
    try:
        result = subprocess.run([
            "uv", "run", "python", "bin/run_tests.py", "--unit"
        ], check=True)
        
        if result.returncode == 0:
            print("✅ All unit tests passed!")
        else:
            print("❌ Some unit tests failed!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Unit test execution failed: {e}")


def run_api_tests():
    """Run API tests only."""
    print("\n🌐 Running API tests...")
    
    try:
        result = subprocess.run([
            "uv", "run", "python", "bin/run_tests.py", "--api"
        ], check=True)
        
        if result.returncode == 0:
            print("✅ All API tests passed!")
        else:
            print("❌ Some API tests failed!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ API test execution failed: {e}")


def show_help():
    """Show help information."""
    print("\n📖 Credit Approval System - Help")
    print("-" * 40)
    print("Available commands:")
    print("  start     - Start the development server")
    print("  setup     - Setup database and import data")
    print("  test      - Run all tests (unit + API)")
    print("  unit      - Run unit tests only")
    print("  api       - Run API tests only")
    print("  help      - Show this help message")
    print("\nExamples:")
    print("  python main.py start")
    print("  python main.py setup")
    print("  python main.py test")
    print("  python main.py unit")
    print("  python main.py api")
    print("\nAPI Endpoints:")
    print("  GET  /api/stats/")
    print("  POST /api/register/")
    print("  POST /api/check-eligibility/")
    print("  POST /api/create-loan/")
    print("  GET  /api/view-loan/<loan_id>/")
    print("  GET  /api/view-loans/<customer_id>/")


def main():
    """Main application entry point."""
    print_banner()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Credit Approval System - Main Launcher",
        add_help=False
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="start",
        choices=["start", "setup", "test", "unit", "api", "help"],
        help="Command to execute (default: start)"
    )
    
    args = parser.parse_args()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Execute the requested command
    if args.command == "start":
        start_server()
    elif args.command == "setup":
        if setup_system():
            print("\n🎉 Setup completed! You can now start the server with:")
            print("   python main.py start")
    elif args.command == "test":
        run_tests()
    elif args.command == "unit":
        run_unit_tests()
    elif args.command == "api":
        run_api_tests()
    elif args.command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {args.command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
