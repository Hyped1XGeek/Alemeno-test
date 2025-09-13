#!/usr/bin/env python3
"""
Test script to verify the corrected credit scoring and loan approval logic.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from credit_system.models import Customer
from credit_system.services.credit_scoring import CreditScoringService
from decimal import Decimal

def main():
    print("🧪 Testing Corrected Credit Scoring Logic...")
    
    # Get customer 316
    customer = Customer.objects.get(customer_id=316)
    
    print(f"📊 Customer 316 Details:")
    print(f"   Name: {customer.full_name}")
    print(f"   Monthly Income: Rs.{customer.monthly_income}")
    print(f"   Current Debt: Rs.{customer.current_debt}")
    
    # Calculate credit score
    credit_score = CreditScoringService.calculate_credit_score(customer)
    print(f"   Credit Score: {credit_score}/100")
    
    # Test different loan scenarios
    test_cases = [
        {"amount": 1000, "rate": 5.0, "tenure": 48, "description": "Small loan, low rate"},
        {"amount": 1000, "rate": 12.0, "tenure": 48, "description": "Small loan, 12% rate"},
        {"amount": 1000, "rate": 16.0, "tenure": 48, "description": "Small loan, 16% rate"},
        {"amount": 1000, "rate": 20.0, "tenure": 48, "description": "Small loan, 20% rate"},
    ]
    
    print(f"\n🧪 Testing Loan Approval Scenarios:")
    print(f"   Credit Score: {credit_score}")
    print(f"   Expected behavior:")
    if credit_score > 50:
        print(f"     - Should approve any interest rate")
    elif credit_score > 30:
        print(f"     - Should approve only if interest rate > 12%")
    elif credit_score > 10:
        print(f"     - Should approve only if interest rate > 16%")
    else:
        print(f"     - Should reject all loans")
    
    print(f"\n📋 Test Results:")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['description']}")
        print(f"     Amount: Rs.{test_case['amount']}")
        print(f"     Rate: {test_case['rate']}%")
        print(f"     Tenure: {test_case['tenure']} months")
        
        approved, message, corrected_rate = CreditScoringService.check_loan_approval(
            customer,
            Decimal(str(test_case['amount'])),
            Decimal(str(test_case['rate'])),
            test_case['tenure']
        )
        
        print(f"     Result: {'✅ APPROVED' if approved else '❌ REJECTED'}")
        print(f"     Message: {message}")
        print(f"     Corrected Rate: {corrected_rate}%")
        
        # Calculate EMI with corrected rate
        emi = CreditScoringService.calculate_monthly_emi(
            Decimal(str(test_case['amount'])), 
            corrected_rate, 
            test_case['tenure']
        )
        print(f"     Monthly EMI: Rs.{emi}")

if __name__ == "__main__":
    main()
