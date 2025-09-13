#!/usr/bin/env python3
"""
Test script for the Credit Approval System API endpoints.

This script tests all the API endpoints as specified in the assignment requirements.
"""

import json

import requests

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_register():
    """Test the /register endpoint."""
    print("🧪 Testing /register endpoint...")

    url = f"{BASE_URL}/register/"
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "monthly_income": 75000,
        "phone_number": "9876543212"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 201:
            print("✅ Register endpoint working correctly")
            return response.json().get("customer_id")
        else:
            print("❌ Register endpoint failed")
            return None

    except Exception as e:
        print(f"❌ Error testing register: {e}")
        return None

def test_check_eligibility(customer_id):
    """Test the /check-eligibility endpoint."""
    print(f"\n🧪 Testing /check-eligibility endpoint for customer {customer_id}...")

    url = f"{BASE_URL}/check-eligibility/"
    data = {
        "customer_id": customer_id,
        "loan_amount": 100000,
        "interest_rate": 12.5,
        "tenure": 24
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ Check eligibility endpoint working correctly")
            return response.json()
        else:
            print("❌ Check eligibility endpoint failed")
            return None

    except Exception as e:
        print(f"❌ Error testing check eligibility: {e}")
        return None

def test_create_loan(customer_id):
    """Test the /create-loan endpoint."""
    print(f"\n🧪 Testing /create-loan endpoint for customer {customer_id}...")

    url = f"{BASE_URL}/create-loan/"
    data = {
        "customer_id": customer_id,
        "loan_amount": 100000,
        "interest_rate": 12.5,
        "tenure": 24
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code in [201, 400]:  # 201 for approved, 400 for rejected
            print("✅ Create loan endpoint working correctly")
            return response.json()
        else:
            print("❌ Create loan endpoint failed")
            return None

    except Exception as e:
        print(f"❌ Error testing create loan: {e}")
        return None

def test_view_loan(loan_id):
    """Test the /view-loan/{loan_id} endpoint."""
    print(f"\n🧪 Testing /view-loan/{loan_id} endpoint...")

    url = f"{BASE_URL}/view-loan/{loan_id}/"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ View loan endpoint working correctly")
            return response.json()
        else:
            print("❌ View loan endpoint failed")
            return None

    except Exception as e:
        print(f"❌ Error testing view loan: {e}")
        return None

def test_view_customer_loans(customer_id):
    """Test the /view-loans/{customer_id} endpoint."""
    print(f"\n🧪 Testing /view-loans/{customer_id} endpoint...")

    url = f"{BASE_URL}/view-loans/{customer_id}/"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ View customer loans endpoint working correctly")
            return response.json()
        else:
            print("❌ View customer loans endpoint failed")
            return None

    except Exception as e:
        print(f"❌ Error testing view customer loans: {e}")
        return None

def test_system_stats():
    """Test the /stats/ endpoint."""
    print("\n🧪 Testing /stats/ endpoint...")

    url = f"{BASE_URL}/stats/"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ System stats endpoint working correctly")
            return response.json()
        else:
            print("❌ System stats endpoint failed")
            return None

    except Exception as e:
        print(f"❌ Error testing system stats: {e}")
        return None

def test_existing_customer():
    """Test with existing customer data."""
    print("\n🧪 Testing with existing customer (ID: 1)...")

    # Test check eligibility with existing customer
    eligibility_result = test_check_eligibility(1)

    # Test create loan with existing customer
    loan_result = test_create_loan(1)

    # Test view customer loans
    test_view_customer_loans(1)

    # If loan was created, test view loan
    if loan_result and loan_result.get("loan_id"):
        test_view_loan(loan_result["loan_id"])

def main():
    """Main test function."""
    print("🚀 Starting Credit Approval System API Tests")
    print("=" * 50)

    # Test system stats first
    test_system_stats()

    # Test with existing customer
    test_existing_customer()

    # Test new customer registration
    print("\n🧪 Testing new customer registration...")
    customer_id = test_register()

    if customer_id:
        # Test eligibility check
        test_check_eligibility(customer_id)

        # Test loan creation
        loan_result = test_create_loan(customer_id)

        # Test view customer loans
        test_view_customer_loans(customer_id)

        # If loan was created, test view loan
        if loan_result and loan_result.get("loan_id"):
            test_view_loan(loan_result["loan_id"])

    print("\n" + "=" * 50)
    print("🏁 API Testing Complete!")

if __name__ == "__main__":
    main()
