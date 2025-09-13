#!/usr/bin/env python3
"""
Test script to verify the approved limit calculation fix.
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
from decimal import Decimal

def main():
    print("🧪 Testing Approved Limit Calculation...")
    
    # Test cases
    test_cases = [
        {"income": 5000, "expected": 200000, "description": "₹5,000 → ₹200,000 (36×5000=180,000 → 200,000)"},
        {"income": 6000, "expected": 200000, "description": "₹6,000 → ₹200,000 (36×6000=216,000 → 200,000)"},
        {"income": 7000, "expected": 300000, "description": "₹7,000 → ₹300,000 (36×7000=252,000 → 300,000)"},
        {"income": 10000, "expected": 400000, "description": "₹10,000 → ₹400,000 (36×10000=360,000 → 400,000)"},
        {"income": 15000, "expected": 500000, "description": "₹15,000 → ₹500,000 (36×15000=540,000 → 500,000)"},
        {"income": 20000, "expected": 700000, "description": "₹20,000 → ₹700,000 (36×20000=720,000 → 700,000)"},
    ]
    
    print(f"📊 Testing Approved Limit Calculations:")
    
    for i, test_case in enumerate(test_cases, 1):
        monthly_income = Decimal(str(test_case['income']))
        expected = test_case['expected']
        description = test_case['description']
        
        # Calculate using the fixed method
        calculated = Customer.calculate_approved_limit(monthly_income)
        
        # Show calculation steps
        base_limit = monthly_income * 36
        lakhs = round(base_limit / Decimal('100000'))
        
        print(f"\n   Test {i}: {description}")
        print(f"     Monthly Income: ₹{monthly_income}")
        print(f"     36 × Income: ₹{base_limit}")
        print(f"     Lakhs: {lakhs}")
        print(f"     Calculated Limit: ₹{calculated}")
        print(f"     Expected Limit: ₹{expected}")
        print(f"     Result: {'✅ CORRECT' if calculated == expected else '❌ INCORRECT'}")
    
    # Test with existing customer 316
    print(f"\n📋 Testing Customer 316:")
    try:
        customer = Customer.objects.get(customer_id=316)
        print(f"   Current Monthly Income: ₹{customer.monthly_income}")
        print(f"   Current Approved Limit: ₹{customer.approved_limit}")
        
        # Calculate what it should be
        correct_limit = Customer.calculate_approved_limit(customer.monthly_income)
        print(f"   Correct Approved Limit: ₹{correct_limit}")
        print(f"   Needs Update: {'Yes' if customer.approved_limit != correct_limit else 'No'}")
        
    except Customer.DoesNotExist:
        print("   Customer 316 not found!")

if __name__ == "__main__":
    main()
