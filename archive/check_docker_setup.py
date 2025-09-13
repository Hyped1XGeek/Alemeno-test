#!/usr/bin/env python3
"""
Check Docker PostgreSQL setup and connectivity.
This script helps diagnose connection issues.
"""

import socket
import subprocess

import psycopg2


def check_docker_running():
    """Check if Docker is running and PostgreSQL container is up."""
    print("🐳 Checking Docker setup...")

    try:
        # Check if docker command is available
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Docker is not installed or not in PATH")
            return False

        print(f"✅ Docker found: {result.stdout.strip()}")

        # Check running containers
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'],
                              capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            print("❌ Failed to list Docker containers")
            return False

        print("📋 Running containers:")
        print(result.stdout)

        # Check for PostgreSQL container
        if 'postgres' in result.stdout.lower() or 'db' in result.stdout.lower():
            print("✅ PostgreSQL container found")
            return True
        else:
            print("⚠️  No PostgreSQL container found")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Docker command timed out")
        return False
    except FileNotFoundError:
        print("❌ Docker command not found")
        return False
    except Exception as e:
        print(f"❌ Error checking Docker: {e}")
        return False


def check_port_connectivity():
    """Check if port 5432 is accessible."""
    print("\n🔌 Checking port connectivity...")

    try:
        # Try to connect to localhost:5432
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 5432))
        sock.close()

        if result == 0:
            print("✅ Port 5432 is accessible")
            return True
        else:
            print("❌ Port 5432 is not accessible")
            return False

    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return False


def check_database_connection():
    """Test actual database connection."""
    print("\n🐘 Testing database connection...")

    try:
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='credit_system',
            user='postgres',
            password='postgres',
            connect_timeout=10
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print("✅ Database connection successful!")
        print(f"PostgreSQL Version: {version[0]}")

        cursor.close()
        connection.close()
        return True

    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def suggest_solutions():
    """Provide troubleshooting suggestions."""
    print("\n🔧 Troubleshooting suggestions:")
    print("1. Start Docker Desktop if not running")
    print("2. Start PostgreSQL container:")
    print("   docker-compose up -d db")
    print("3. Check container logs:")
    print("   docker-compose logs db")
    print("4. Verify container is healthy:")
    print("   docker-compose ps")
    print("5. Try connecting directly:")
    print("   docker exec -it <container_name> psql -U postgres -d credit_system")


def main():
    """Main diagnostic function."""
    print("🔍 PostgreSQL Docker Setup Diagnostic")
    print("=" * 50)

    docker_ok = check_docker_running()
    port_ok = check_port_connectivity()
    db_ok = check_database_connection()

    print("\n" + "=" * 50)
    print("📊 Diagnostic Summary:")
    print(f"Docker: {'✅' if docker_ok else '❌'}")
    print(f"Port 5432: {'✅' if port_ok else '❌'}")
    print(f"Database: {'✅' if db_ok else '❌'}")

    if all([docker_ok, port_ok, db_ok]):
        print("\n🎉 Everything looks good! Your PostgreSQL setup is working.")
    else:
        print("\n⚠️  Some issues detected. See suggestions below:")
        suggest_solutions()


if __name__ == "__main__":
    main()
