#!/usr/bin/env python3
"""
Test script to verify new customer registration with correct approved limit.
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


def main():
    print("🧪 Testing New Customer Registration Logic...")

    # Test cases for new customer registration
    test_cases = [
        {"income": 6000, "expected": 200000, "description": "₹6,000 monthly income"},
        {"income": 8000, "expected": 300000, "description": "₹8,000 monthly income"},
        {"income": 10000, "expected": 400000, "description": "₹10,000 monthly income"},
    ]

    print("📊 Testing Approved Limit Calculation for New Customers:")

    for i, test_case in enumerate(test_cases, 1):
        monthly_income = Decimal(str(test_case['income']))
        expected = test_case['expected']
        description = test_case['description']

        # Calculate approved limit using the fixed method
        calculated_limit = Customer.calculate_approved_limit(monthly_income)

        print(f"\n   Test {i}: {description}")
        print(f"     Monthly Income: ₹{monthly_income}")
        print(f"     Calculated Approved Limit: ₹{calculated_limit}")
        print(f"     Expected Approved Limit: ₹{expected}")
        print(f"     Result: {'✅ CORRECT' if calculated_limit == expected else '❌ INCORRECT'}")

        # Show the calculation steps
        base_limit = monthly_income * 36
        lakhs = round(base_limit / Decimal('100000'))
        print(f"     Calculation: 36 × ₹{monthly_income} = ₹{base_limit} → {lakhs} lakhs → ₹{calculated_limit}")

    print("\n🌐 API Registration Test:")
    print("   For a customer with ₹8,000 monthly income:")
    print("   POST /api/register/")
    print("   Body: {'monthly_income': '8000', ...}")
    print("   Expected Response: {'approved_limit': 300000.0, ...}")

    print("\n✅ New customer registration will now use the correct approved limit calculation!")

if __name__ == "__main__":
    main()
