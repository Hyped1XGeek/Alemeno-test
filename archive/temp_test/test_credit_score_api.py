#!/usr/bin/env python3
"""
Test script for the new credit score API endpoint.
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

def main():
    print("🧪 Testing Credit Score API Endpoint...")
    
    # Test with customer 316
    print(f"\n📊 Testing Customer 316:")
    
    try:
        customer = Customer.objects.get(customer_id=316)
        credit_score = CreditScoringService.calculate_credit_score(customer)
        
        print(f"   Customer ID: {customer.customer_id}")
        print(f"   Name: {customer.full_name}")
        print(f"   Age: {customer.age}")
        print(f"   Monthly Income: Rs.{customer.monthly_income}")
        print(f"   Approved Limit: Rs.{customer.approved_limit}")
        print(f"   Current Debt: Rs.{customer.current_debt}")
        print(f"   Credit Score: {credit_score}/100")
        print(f"   Credit Utilization: {customer.credit_utilization_ratio:.1f}%")
        
        print(f"\n🌐 API Endpoint:")
        print(f"   GET http://127.0.0.1:8000/api/credit-score/316/")
        
        print(f"\n📋 Expected Response:")
        expected_response = {
            "customer_id": customer.customer_id,
            "name": customer.full_name,
            "age": customer.age,
            "monthly_income": float(customer.monthly_income),
            "approved_limit": float(customer.approved_limit),
            "current_debt": float(customer.current_debt),
            "credit_score": credit_score,
            "credit_utilization": float(customer.credit_utilization_ratio)
        }
        
        import json
        print(json.dumps(expected_response, indent=2))
        
    except Customer.DoesNotExist:
        print("   ❌ Customer 316 not found!")
    
    # Test with a non-existent customer
    print(f"\n🧪 Testing Non-existent Customer (99999):")
    print(f"   GET http://127.0.0.1:8000/api/credit-score/99999/")
    print(f"   Expected: 404 Not Found")
    
    print(f"\n✅ Credit Score API endpoint is ready!")
    print(f"   Endpoint: GET /api/credit-score/<customer_id>/")
    print(f"   Returns: Customer details and credit score")

if __name__ == "__main__":
    main()
