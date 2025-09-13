"""
Test configuration for Credit Approval System.

This module provides configuration for different testing strategies:
1. Database rollback (default) - Fast, uses same DB with rollback
2. Separate test database - Complete isolation, more realistic
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
from django.conf import settings
from django.test.utils import get_runner
from django.db import connection


class TestConfig:
    """Configuration for different testing strategies."""
    
    @staticmethod
    def setup_rollback_testing():
        """Setup for database rollback testing (default)."""
        print("🧪 Setting up ROLLBACK testing...")
        print("   - Uses same database with automatic rollback")
        print("   - Fast execution")
        print("   - All changes are reverted after each test")
        print("   - Best for unit tests and development")
        
        # Ensure we're using the main database
        settings.DATABASES['default']['NAME'] = 'credit_system'
        
    @staticmethod
    def setup_separate_test_db():
        """Setup for separate test database."""
        print("🧪 Setting up SEPARATE TEST DATABASE...")
        print("   - Creates isolated test database")
        print("   - Complete isolation from main data")
        print("   - More realistic testing")
        print("   - Best for integration tests and production")
        
        # Create test database name
        test_db_name = f"test_{settings.DATABASES['default']['NAME']}"
        settings.DATABASES['default']['NAME'] = test_db_name
        
        # Create test database
        connection.creation.create_test_db(verbosity=1, autoclobber=True)
        
    @staticmethod
    def cleanup_separate_test_db():
        """Cleanup separate test database."""
        if hasattr(connection, 'creation'):
            connection.creation.destroy_test_db(
                settings.DATABASES['default']['NAME'], 
                verbosity=1
            )


def run_tests_with_rollback(test_labels=None, verbosity=1, interactive=True, keepdb=False, **kwargs):
    """Run tests with database rollback (default behavior)."""
    TestConfig.setup_rollback_testing()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=interactive, keepdb=keepdb)
    
    failures = test_runner.run_tests(test_labels)
    return failures


def run_tests_with_separate_db(test_labels=None, verbosity=1, interactive=True, keepdb=False, **kwargs):
    """Run tests with separate test database."""
    TestConfig.setup_separate_test_db()
    
    try:
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=verbosity, interactive=interactive, keepdb=keepdb)
        
        failures = test_runner.run_tests(test_labels)
        return failures
    finally:
        if not keepdb:
            TestConfig.cleanup_separate_test_db()


def run_tests(test_labels=None, verbosity=1, interactive=True, keepdb=False, separate_db=False, **kwargs):
    """
    Run tests with specified strategy.
    
    Args:
        test_labels: List of test labels to run
        verbosity: Verbosity level (0-2)
        interactive: Whether to allow interactive prompts
        keepdb: Whether to keep test database after tests
        separate_db: Whether to use separate test database
    """
    if separate_db:
        return run_tests_with_separate_db(test_labels, verbosity, interactive, keepdb, **kwargs)
    else:
        return run_tests_with_rollback(test_labels, verbosity, interactive, keepdb, **kwargs)
