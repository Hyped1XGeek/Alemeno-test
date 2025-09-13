#!/usr/bin/env python3
"""
Test script to verify EMI validation with corrected interest rate.
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
    print("🧪 Testing EMI Validation with Corrected Interest Rate...")
    
    # Get customer 316
    customer = Customer.objects.get(customer_id=316)
    
    print(f"📊 Customer 316 Details:")
    print(f"   Name: {customer.full_name}")
    print(f"   Monthly Income: Rs.{customer.monthly_income}")
    print(f"   50% of Monthly Income: Rs.{customer.monthly_income * Decimal('0.5')}")
    print(f"   Current Debt: Rs.{customer.current_debt}")
    
    # Get current monthly EMIs
    current_loans = customer.loans.filter(end_date__gte=date.today())
    current_monthly_emis = sum(loan.monthly_installment for loan in current_loans)
    print(f"   Current Monthly EMIs: Rs.{current_monthly_emis}")
    
    # Test the problematic case: ₹100,000 loan at 1% interest
    print(f"\n🧪 Testing ₹100,000 loan at 1% interest:")
    
    approved, message, corrected_rate = CreditScoringService.check_loan_approval(
        customer,
        Decimal('100000.00'),  # ₹100,000
        Decimal('1.0'),        # 1% interest
        48                     # 48 months
    )
    
    print(f"   Result: {'✅ APPROVED' if approved else '❌ REJECTED'}")
    print(f"   Message: {message}")
    print(f"   Corrected Rate: {corrected_rate}%")
    
    # Calculate EMI with corrected rate
    emi = CreditScoringService.calculate_monthly_emi(
        Decimal('100000.00'), 
        corrected_rate, 
        48
    )
    print(f"   Monthly EMI: Rs.{emi}")
    
    # Calculate total EMIs
    total_emis = current_monthly_emis + emi
    print(f"   Total Monthly EMIs: Rs.{total_emis}")
    print(f"   50% of Income: Rs.{customer.monthly_income * Decimal('0.5')}")
    print(f"   Exceeds 50%: {'Yes' if total_emis > customer.monthly_income * Decimal('0.5') else 'No'}")

if __name__ == "__main__":
    from datetime import date
    main()
