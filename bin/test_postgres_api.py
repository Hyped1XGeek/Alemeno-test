#!/usr/bin/env python3
"""
Comprehensive API test script for Credit Approval System with PostgreSQL.
Tests all endpoints and verifies data integrity.
"""

import requests
import json
import time
import sys
from datetime import datetime


class CreditSystemAPITester:
    """Test class for Credit Approval System API."""
    
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_customer_id = None
        self.test_loan_id = None
        
    def test_connection(self):
        """Test if the API server is running."""
        try:
            response = self.session.get(f"{self.base_url}/api/stats/", timeout=5)
            if response.status_code == 200:
                print("✅ API server is running")
                return True
            else:
                print(f"❌ API server returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to API server: {e}")
            return False
    
    def test_stats_endpoint(self):
        """Test the stats endpoint."""
        print("\n📊 Testing /api/stats/ endpoint...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/stats/")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Stats endpoint working")
                print(f"   Total customers: {data.get('total_customers', 'N/A')}")
                print(f"   Total loans: {data.get('total_loans', 'N/A')}")
                print(f"   Active loans: {data.get('active_loans', 'N/A')}")
                print(f"   Total loan amount: ₹{data.get('total_loan_amount', 'N/A'):,}")
                return True
            else:
                print(f"❌ Stats endpoint failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Stats endpoint error: {e}")
            return False
    
    def test_register_endpoint(self):
        """Test the customer registration endpoint."""
        print("\n👤 Testing /api/register/ endpoint...")
        
        # Test data
        customer_data = {
            "first_name": "Test",
            "last_name": "User",
            "age": 30,
            "monthly_income": 50000,
            "phone_number": f"9999{int(time.time())}",  # Unique phone number
            "approved_limit": 100000
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/register/",
                json=customer_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.test_customer_id = data.get('customer_id')
                print("✅ Customer registration successful")
                print(f"   Customer ID: {self.test_customer_id}")
                print(f"   Name: {data.get('first_name')} {data.get('last_name')}")
                print(f"   Approved Limit: ₹{data.get('approved_limit'):,}")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def test_check_eligibility_endpoint(self):
        """Test the loan eligibility check endpoint."""
        print("\n🔍 Testing /api/check-eligibility/ endpoint...")
        
        if not self.test_customer_id:
            print("❌ No test customer ID available")
            return False
        
        eligibility_data = {
            "customer_id": self.test_customer_id,
            "loan_amount": 50000,
            "interest_rate": 12.0,
            "tenure": 12
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/check-eligibility/",
                json=eligibility_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Eligibility check successful")
                print(f"   Customer ID: {data.get('customer_id')}")
                print(f"   Approval: {data.get('approval')}")
                print(f"   Interest Rate: {data.get('interest_rate')}%")
                print(f"   Corrected Interest Rate: {data.get('corrected_interest_rate')}%")
                monthly_installment = data.get('monthly_installment')
                if monthly_installment is not None:
                    print(f"   Monthly Installment: ₹{monthly_installment:,}")
                return True
            else:
                print(f"❌ Eligibility check failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Eligibility check error: {e}")
            return False
    
    def test_create_loan_endpoint(self):
        """Test the loan creation endpoint."""
        print("\n💰 Testing /api/create-loan/ endpoint...")
        
        if not self.test_customer_id:
            print("❌ No test customer ID available")
            return False
        
        loan_data = {
            "customer_id": self.test_customer_id,
            "loan_amount": 50000,
            "interest_rate": 12.0,
            "tenure": 12
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/create-loan/",
                json=loan_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.test_loan_id = data.get('loan_id')
                print("✅ Loan creation successful")
                print(f"   Loan ID: {self.test_loan_id}")
                print(f"   Customer ID: {data.get('customer_id')}")
                print(f"   Loan Approved: {data.get('loan_approved')}")
                print(f"   Message: {data.get('message')}")
                monthly_installment = data.get('monthly_installment')
                
                if monthly_installment is not None:
                    print(f"   Monthly Installment: ₹{monthly_installment:,}")
                return True
            else:
                print(f"❌ Loan creation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Loan creation error: {e}")
            return False
    
    def test_view_loan_endpoint(self):
        """Test the view loan endpoint."""
        print("\n👁️ Testing /api/view-loan/<loan_id>/ endpoint...")
        
        if not self.test_loan_id:
            print("❌ No test loan ID available")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/api/view-loan/{self.test_loan_id}/")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ View loan successful")
                print(f"   Loan ID: {data.get('loan_id')}")
                print(f"   Customer ID: {data.get('customer_id')}")
                loan_amount = data.get('loan_amount')
                interest_rate = data.get('interest_rate')
                monthly_installment = data.get('monthly_installment')
                tenure = data.get('tenure')
                
                if loan_amount is not None:
                    print(f"   Loan Amount: ₹{loan_amount:,}")
                if interest_rate is not None:
                    print(f"   Interest Rate: {interest_rate}%")
                if monthly_installment is not None:
                    print(f"   Monthly Installment: ₹{monthly_installment:,}")
                if tenure is not None:
                    print(f"   Tenure: {tenure} months")
                return True
            else:
                print(f"❌ View loan failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ View loan error: {e}")
            return False
    
    def test_view_loans_endpoint(self):
        """Test the view customer loans endpoint."""
        print("\n📋 Testing /api/view-loans/<customer_id>/ endpoint...")
        
        if not self.test_customer_id:
            print("❌ No test customer ID available")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/api/view-loans/{self.test_customer_id}/")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ View customer loans successful")
                print(f"   Customer ID: {data.get('customer_id')}")
                print(f"   Name: {data.get('first_name')} {data.get('last_name')}")
                print(f"   Total Loans: {len(data.get('loans', []))}")
                
                loans = data.get('loans', [])
                if loans:
                    loan = loans[0]
                    print(f"   First Loan ID: {loan.get('loan_id')}")
                    print(f"   First Loan Amount: ₹{loan.get('loan_amount'):,}")
                
                return True
            else:
                print(f"❌ View customer loans failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ View customer loans error: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid requests."""
        print("\n🚨 Testing error handling...")
        
        success = True
        
        # Test invalid customer ID
        try:
            response = self.session.get(f"{self.base_url}/api/view-loans/99999/")
            if response.status_code == 404:
                print("✅ Invalid customer ID handled correctly (404)")
            else:
                print(f"❌ Expected 404, got {response.status_code}")
                success = False
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            success = False
        
        # Test invalid loan ID
        try:
            response = self.session.get(f"{self.base_url}/api/view-loan/99999/")
            if response.status_code == 404:
                print("✅ Invalid loan ID handled correctly (404)")
            else:
                print(f"❌ Expected 404, got {response.status_code}")
                success = False
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            success = False
        
        return success
    
    def run_all_tests(self):
        """Run all API tests."""
        print("🧪 Credit Approval System - PostgreSQL API Tests")
        print("=" * 60)
        
        tests = [
            ("Connection Test", self.test_connection),
            ("Stats Endpoint", self.test_stats_endpoint),
            ("Register Endpoint", self.test_register_endpoint),
            ("Check Eligibility", self.test_check_eligibility_endpoint),
            ("Create Loan", self.test_create_loan_endpoint),
            ("View Loan", self.test_view_loan_endpoint),
            ("View Customer Loans", self.test_view_loans_endpoint),
            ("Error Handling", self.test_error_handling),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name} PASSED")
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")
        
        print(f"\n{'='*60}")
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! PostgreSQL integration is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Please check the errors above.")
            return False


def main():
    """Main test function."""
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    tester = CreditSystemAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Your Credit Approval System is ready!")
        print("📋 Available endpoints:")
        print("   GET  /api/stats/")
        print("   POST /api/register/")
        print("   POST /api/check-eligibility/")
        print("   POST /api/create-loan/")
        print("   GET  /api/view-loan/<loan_id>/")
        print("   GET  /api/view-loans/<customer_id>/")
        print("\n🌐 Access your API at: http://127.0.0.1:8000/api/")
        print("🔧 Admin interface: http://127.0.0.1:8000/admin/")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
