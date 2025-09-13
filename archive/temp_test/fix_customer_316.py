#!/usr/bin/env python3
"""
Temporary script to fix customer 316's approved limit and test loan approval.
"""

import os
import sys

import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from decimal import Decimal

from credit_system.models import Customer
from credit_system.services.credit_scoring import CreditScoringService


def main():
    print("🔍 Checking Customer 316...")

    # Get customer 316
    try:
        customer = Customer.objects.get(customer_id=316)
    except Customer.DoesNotExist:
        print("❌ Customer 316 not found!")
        return

    print("📊 Current Customer Data:")
    print(f"   Name: {customer.full_name}")
    print(f"   Age: {customer.age}")
    print(f"   Monthly Income: Rs.{customer.monthly_income}")
    print(f"   Current Approved Limit: Rs.{customer.approved_limit}")
    print(f"   Current Debt: Rs.{customer.current_debt}")

    # Calculate what the approved limit should be
    correct_limit = Customer.calculate_approved_limit(customer.monthly_income)
    print(f"   Correct Approved Limit: Rs.{correct_limit}")

    # Check if the limit needs to be updated
    if customer.approved_limit != correct_limit:
        print(f"\n🔧 Updating approved limit from Rs.{customer.approved_limit} to Rs.{correct_limit}")
        customer.approved_limit = correct_limit
        customer.save()
        print("✅ Approved limit updated!")
    else:
        print("✅ Approved limit is already correct!")

    # Calculate credit utilization
    utilization = (customer.current_debt / customer.approved_limit) * 100
    print("\n📈 Credit Analysis:")
    print(f"   Credit Utilization: {utilization:.1f}%")
    print(f"   80% Limit: Rs.{customer.approved_limit * Decimal('0.8')}")

    # Test new loan eligibility
    print("\n🧪 Testing New Loan Eligibility:")
    print("   Requested Amount: Rs.1,000")
    print("   Interest Rate: 5.0%")
    print("   Tenure: 48 months")

    approved, message, corrected_rate = CreditScoringService.check_loan_approval(
        customer,
        Decimal('1000.00'),
        Decimal('5.0'),
        48
    )

    print(f"   Result: {'✅ APPROVED' if approved else '❌ REJECTED'}")
    print(f"   Message: {message}")
    print(f"   Corrected Rate: {corrected_rate}%")

    # Calculate total debt with new loan
    total_debt = customer.current_debt + Decimal('1000.00')
    new_utilization = (total_debt / customer.approved_limit) * 100
    print(f"   Total Debt with New Loan: Rs.{total_debt}")
    print(f"   New Credit Utilization: {new_utilization:.1f}%")

if __name__ == "__main__":
    main()
