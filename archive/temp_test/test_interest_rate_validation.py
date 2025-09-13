#!/usr/bin/env python3
"""
Test script to verify interest rate validation logic.
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
    print("🧪 Testing Interest Rate Validation Logic...")

    # Get customer 316
    customer = Customer.objects.get(customer_id=316)
    credit_score = CreditScoringService.calculate_credit_score(customer)

    print("📊 Customer 316 Details:")
    print(f"   Credit Score: {credit_score}/100")
    print(f"   Monthly Income: Rs.{customer.monthly_income}")
    print(f"   Current Monthly EMIs: Rs.{sum(loan.monthly_installment for loan in customer.loans.filter(end_date__gte=date.today()))}")

    # Test different interest rates
    test_cases = [
        {"rate": 1.0, "amount": 20000, "description": "1% rate - should be REJECTED"},
        {"rate": 5.0, "amount": 20000, "description": "5% rate - should be REJECTED"},
        {"rate": 12.0, "amount": 20000, "description": "12% rate - should be APPROVED"},
        {"rate": 15.0, "amount": 20000, "description": "15% rate - should be APPROVED"},
    ]

    print("\n🧪 Testing Loan Approval with Different Interest Rates:")
    print(f"   Credit Score: {credit_score} (requires interest rate >= 12%)")

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['description']}")
        print(f"     Amount: Rs.{test_case['amount']}")
        print(f"     Requested Rate: {test_case['rate']}%")

        approved, message, corrected_rate = CreditScoringService.check_loan_approval(
            customer,
            Decimal(str(test_case['amount'])),
            Decimal(str(test_case['rate'])),
            48
        )

        print(f"     Result: {'✅ APPROVED' if approved else '❌ REJECTED'}")
        print(f"     Message: {message}")
        print(f"     Corrected Rate: {corrected_rate}%")

        # Calculate EMI with corrected rate
        emi = CreditScoringService.calculate_monthly_emi(
            Decimal(str(test_case['amount'])),
            corrected_rate,
            48
        )
        print(f"     Monthly EMI: Rs.{emi}")

if __name__ == "__main__":
    from datetime import date
    main()
