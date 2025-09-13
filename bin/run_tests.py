#!/usr/bin/env python3
"""
Comprehensive test runner for Credit Approval System.

This script provides different testing strategies:
1. Unit tests with database rollback (default)
2. Integration tests with separate test database
3. API tests (existing)
4. All tests combined

Usage:
    python bin/run_tests.py                    # Run unit tests (rollback)
    python bin/run_tests.py --separate-db      # Run with separate test DB
    python bin/run_tests.py --api              # Run API tests
    python bin/run_tests.py --all              # Run all tests
    python bin/run_tests.py --help             # Show help
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from tests.test_config import run_tests


def run_unit_tests(separate_db=False, verbosity=1):
    """Run unit tests for models and services."""
    print("🧪 Running Unit Tests...")
    print("=" * 60)
    
    test_labels = [
        'tests.test_models',
        'tests.test_services'
    ]
    
    failures = run_tests(
        test_labels=test_labels,
        verbosity=verbosity,
        separate_db=separate_db
    )
    
    if failures:
        print(f"❌ {failures} unit test(s) failed")
        return False
    else:
        print("✅ All unit tests passed!")
        return True


def run_api_tests():
    """Run API integration tests."""
    print("\n🌐 Running API Tests...")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            "uv", "run", "python", "tests/test_api.py"
        ], check=True, capture_output=True, text=True)
        
        print(result.stdout)
        print("✅ All API tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ API tests failed:")
        print(e.stdout)
        print(e.stderr)
        return False


def run_all_tests(separate_db=False, verbosity=1):
    """Run all tests (unit + API)."""
    print("🚀 Running All Tests...")
    print("=" * 60)
    
    # Run unit tests
    unit_success = run_unit_tests(separate_db, verbosity)
    
    # Run API tests
    api_success = run_api_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Unit Tests: {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print(f"API Tests:  {'✅ PASSED' if api_success else '❌ FAILED'}")
    
    if unit_success and api_success:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED!")
        return False


def show_help():
    """Show help information."""
    print("🧪 Credit Approval System - Test Runner")
    print("=" * 60)
    print("Available test types:")
    print("  --unit         Run unit tests (models, services)")
    print("  --api          Run API integration tests")
    print("  --all          Run all tests (unit + API)")
    print("")
    print("Test database options:")
    print("  --separate-db  Use separate test database (slower but more realistic)")
    print("  --rollback     Use database rollback (default, faster)")
    print("")
    print("Other options:")
    print("  --verbosity N  Set verbosity level (0-2, default: 1)")
    print("  --help         Show this help message")
    print("")
    print("Examples:")
    print("  python bin/run_tests.py                    # Unit tests with rollback")
    print("  python bin/run_tests.py --separate-db      # Unit tests with separate DB")
    print("  python bin/run_tests.py --api              # API tests only")
    print("  python bin/run_tests.py --all              # All tests")
    print("  python bin/run_tests.py --all --separate-db # All tests with separate DB")


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Credit Approval System Test Runner",
        add_help=False
    )
    
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run unit tests (models, services)"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Run API integration tests"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests (unit + API)"
    )
    parser.add_argument(
        "--separate-db",
        action="store_true",
        help="Use separate test database"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Use database rollback (default)"
    )
    parser.add_argument(
        "--verbosity",
        type=int,
        default=1,
        choices=[0, 1, 2],
        help="Verbosity level (0-2)"
    )
    parser.add_argument(
        "--help",
        action="store_true",
        help="Show help message"
    )
    
    args = parser.parse_args()
    
    # Show help if requested
    if args.help or not any([args.unit, args.api, args.all]):
        show_help()
        return 0
    
    # Determine test database strategy
    separate_db = args.separate_db
    
    if separate_db:
        print("🗄️  Using SEPARATE TEST DATABASE")
        print("   - Complete isolation from main data")
        print("   - More realistic testing")
        print("   - Slower execution")
    else:
        print("🔄 Using DATABASE ROLLBACK")
        print("   - Fast execution")
        print("   - All changes reverted after tests")
        print("   - Uses same database structure")
    
    print("")
    
    # Run requested tests
    success = True
    
    if args.unit:
        success = run_unit_tests(separate_db, args.verbosity)
    elif args.api:
        success = run_api_tests()
    elif args.all:
        success = run_all_tests(separate_db, args.verbosity)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
