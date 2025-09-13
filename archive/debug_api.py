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
from credit_system.views import register

def test_register_view():
    """Test the register view directly."""
    factory = RequestFactory()
    
    data = {
        "first_name": "John",
        "last_name": "Doe", 
        "age": 30,
        "monthly_income": 75000,
        "phone_number": "9876543210"
    }
    
    request = factory.post('/api/register/', data, content_type='application/json')
    
    try:
        response = register(request)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_register_view()
