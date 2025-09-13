#!/usr/bin/env python3
"""
API test script for the Credit Approval System.
"""


import requests


def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000/api"

    print("Testing Credit Approval System API...")
    print("=" * 50)

    # Test system stats
    print("1. Testing system stats...")
    try:
        response = requests.get(f"{base_url}/stats/")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ System stats: {stats}")
        else:
            print(f"❌ Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {e}")

    # Test customer list
    print("\n2. Testing customer list...")
    try:
        response = requests.get(f"{base_url}/customers/")
        if response.status_code == 200:
            customers = response.json()
            print(f"✅ Found {len(customers)} customers")
            if customers:
                print(f"First customer: {customers[0]['first_name']} {customers[0]['last_name']}")
        else:
            print(f"❌ Customer list failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Customer list error: {e}")

    # Test credit approval
    print("\n3. Testing credit approval...")
    try:
        approval_data = {
            "customer_id": 1,
            "loan_amount": 50000,
            "tenure": 12,
            "interest_rate": 10.0
        }
        response = requests.post(
            f"{base_url}/credit-approval/",
            json=approval_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code in [200, 400]:  # 400 is expected for rejection
            result = response.json()
            print(f"✅ Credit approval result: {result}")
        else:
            print(f"❌ Credit approval failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Credit approval error: {e}")

    # Test customer detail
    print("\n4. Testing customer detail...")
    try:
        response = requests.get(f"{base_url}/customers/1/")
        if response.status_code == 200:
            customer = response.json()
            print(f"✅ Customer detail: {customer['first_name']} {customer['last_name']}")
            print(f"   Salary: {customer['monthly_salary']}")
            print(f"   Approved Limit: {customer['approved_limit']}")
        else:
            print(f"❌ Customer detail failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Customer detail error: {e}")

    print("\n" + "=" * 50)
    print("API testing completed!")

if __name__ == "__main__":
    test_api()
