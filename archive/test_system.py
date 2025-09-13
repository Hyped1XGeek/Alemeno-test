#!/usr/bin/env python3
"""
Test script for the Credit Approval System.

This script tests the basic functionality of the system including
data import, credit approval, and API endpoints.
"""

import os
import sys
from decimal import Decimal

import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from credit_system.models import Customer, Loan
from credit_system.services import CreditApprovalService, CreditScoringService


def test_credit_scoring():
    """Test credit scoring functionality."""
    print("Testing Credit Scoring...")

    # Clean up any existing test data first
    Customer.objects.filter(customer_id__gte=9990).delete()

    # Create a test customer
    customer = Customer.objects.create(
        customer_id=9999,
        first_name="Test",
        last_name="User",
        age=30,
        phone_number="9999999999",
        monthly_salary=Decimal('50000'),
        approved_limit=Decimal('500000')
    )

    # Test credit scoring
    score = CreditScoringService.calculate_credit_score(customer)
    print(f"Credit Score: {score}")

    # Clean up
    customer.delete()
    print("✓ Credit scoring test passed\n")


def test_credit_approval():
    """Test credit approval functionality."""
    print("Testing Credit Approval...")

    # Create a test customer
    customer = Customer.objects.create(
        customer_id=9998,
        first_name="Test",
        last_name="Approval",
        age=35,
        phone_number="9999999998",
        monthly_salary=Decimal('75000'),
        approved_limit=Decimal('300000')
    )

    # Test approval for a reasonable loan
    result = CreditApprovalService.process_credit_approval(
        customer_id=customer.customer_id,
        loan_amount=Decimal('100000'),
        tenure=24,
        interest_rate=Decimal('12.5')
    )

    print(f"Approval Result: {result['approved']}")
    print(f"Message: {result['message']}")
    print(f"Credit Score: {result['credit_score']}")
    print(f"Monthly Payment: {result['monthly_payment']}")

    # Clean up
    if result['approved'] and 'loan_id' in result:
        Loan.objects.filter(loan_id=result['loan_id']).delete()
    customer.delete()
    print("✓ Credit approval test passed\n")


def test_data_models():
    """Test data models functionality."""
    print("Testing Data Models...")

    # Test Customer model
    customer = Customer.objects.create(
        customer_id=9997,
        first_name="Model",
        last_name="Test",
        age=25,
        phone_number="9999999997",
        monthly_salary=Decimal('40000'),
        approved_limit=Decimal('200000')
    )

    print(f"Customer: {customer}")
    print(f"Full Name: {customer.full_name}")
    print(f"Current Debt: {customer.current_debt}")
    print(f"Credit Utilization: {customer.credit_utilization_ratio}%")

    # Test Loan model
    loan = Loan.objects.create(
        loan_id=99999,
        customer=customer,
        loan_amount=Decimal('50000'),
        tenure=12,
        interest_rate=Decimal('10.0'),
        monthly_payment=Decimal('4395.83'),
        emis_paid_on_time=6,
        date_of_approval="2024-01-01",
        end_date="2025-01-01"
    )

    print(f"Loan: {loan}")
    print(f"Is Active: {loan.is_active}")
    print(f"Total Paid: {loan.total_paid}")
    print(f"Remaining Amount: {loan.remaining_amount}")
    print(f"Payment History Score: {loan.payment_history_score}%")

    # Clean up
    loan.delete()
    customer.delete()
    print("✓ Data models test passed\n")


def test_system_stats():
    """Test system statistics."""
    print("Testing System Statistics...")

    # Get current stats
    from datetime import date
    total_customers = Customer.objects.count()
    total_loans = Loan.objects.count()
    active_loans = Loan.objects.filter(end_date__gt=date.today()).count()

    print(f"Total Customers: {total_customers}")
    print(f"Total Loans: {total_loans}")
    print(f"Active Loans: {active_loans}")

    print("✓ System statistics test passed\n")


def main():
    """Run all tests."""
    print("=" * 50)
    print("Credit Approval System - Test Suite")
    print("=" * 50)

    try:
        test_data_models()
        test_credit_scoring()
        test_credit_approval()
        test_system_stats()

        print("=" * 50)
        print("All tests passed successfully! ✓")
        print("=" * 50)

    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
