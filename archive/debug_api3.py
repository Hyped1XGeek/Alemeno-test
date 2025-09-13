#!/usr/bin/env python3
"""
Debug script for API issues.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import RequestFactory
from credit_system.views import check_eligibility

def test_check_eligibility_view():
    """Test the check eligibility view directly."""
    factory = RequestFactory()
    
    data = {
        "customer_id": 1,
        "loan_amount": 100000,
        "interest_rate": 12.5,
        "tenure": 24
    }
    
    request = factory.post('/api/check-eligibility/', data, content_type='application/json')
    
    try:
        response = check_eligibility(request)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_check_eligibility_view()
