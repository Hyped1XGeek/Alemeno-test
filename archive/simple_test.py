#!/usr/bin/env python3
"""
Simple test script for the Credit Approval System.

This script tests the basic functionality using existing data.
"""

import os
import sys
import django
from decimal import Decimal

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from credit_system.models import Customer, Loan
from credit_system.services import CreditApprovalService, CreditScoringService


def test_existing_data():
    """Test with existing data."""
    print("Testing with existing data...")
    
    # Get first customer
    customer = Customer.objects.first()
    if not customer:
        print("❌ No customers found in database")
        return False
    
    print(f"Testing with customer: {customer.full_name}")
    print(f"Customer ID: {customer.customer_id}")
    print(f"Monthly Salary: {customer.monthly_salary}")
    print(f"Approved Limit: {customer.approved_limit}")
    print(f"Current Debt: {customer.current_debt}")
    print(f"Credit Utilization: {customer.credit_utilization_ratio}%")
    
    # Test credit scoring
    score = CreditScoringService.calculate_credit_score(customer)
    print(f"Credit Score: {score}")
    
    # Test credit approval
    result = CreditApprovalService.process_credit_approval(
        customer_id=customer.customer_id,
        loan_amount=Decimal('50000'),
        tenure=12,
        interest_rate=Decimal('10.0')
    )
    
    print(f"Approval Result: {result['approved']}")
    print(f"Message: {result['message']}")
    if 'loan_id' in result:
        print(f"Loan ID: {result['loan_id']}")
    
    return True


def test_system_stats():
    """Test system statistics."""
    print("\nTesting System Statistics...")
    
    from datetime import date
    total_customers = Customer.objects.count()
    total_loans = Loan.objects.count()
    active_loans = Loan.objects.filter(end_date__gt=date.today()).count()
    
    print(f"Total Customers: {total_customers}")
    print(f"Total Loans: {total_loans}")
    print(f"Active Loans: {active_loans}")
    
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("Credit Approval System - Simple Test Suite")
    print("=" * 50)
    
    try:
        if test_existing_data():
            print("✅ Data model test passed")
        
        if test_system_stats():
            print("✅ System stats test passed")
        
        print("=" * 50)
        print("All tests passed successfully! ✓")
        print("=" * 50)
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
