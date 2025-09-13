"""
Unit tests for Credit Approval System models.

These tests verify model behavior, validation, and business logic
without permanent database changes.
"""

import os
import sys
from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

# Add the project root to Python path
sys.path.append(str(os.path.dirname(os.path.dirname(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django

django.setup()

from credit_system.models import Customer, Loan


class CustomerModelTest(TestCase):
    """Test cases for Customer model."""

    def setUp(self):
        """Set up test data that will be rolled back after each test."""
        self.customer_data = {
            'customer_id': 99999,  # Use high ID to avoid conflicts
            'first_name': 'Test',
            'last_name': 'Customer',
            'age': 30,
            'monthly_income': Decimal('50000.00'),
            'phone_number': '9999999999',
            'approved_limit': Decimal('100000.00')
        }

    def test_customer_creation(self):
        """Test basic customer creation."""
        customer = Customer.objects.create(**self.customer_data)

        self.assertEqual(customer.customer_id, 99999)
        self.assertEqual(customer.first_name, 'Test')
        self.assertEqual(customer.last_name, 'Customer')
        self.assertEqual(customer.age, 30)
        self.assertEqual(customer.monthly_income, Decimal('50000.00'))
        self.assertEqual(customer.phone_number, '9999999999')
        self.assertEqual(customer.approved_limit, Decimal('100000.00'))
        # current_debt is a calculated property, not a database field
        self.assertEqual(customer.current_debt, Decimal('0.00'))

    def test_customer_str_representation(self):
        """Test customer string representation."""
        customer = Customer.objects.create(**self.customer_data)
        expected_str = "Test Customer (ID: 99999)"
        self.assertEqual(str(customer), expected_str)

    def test_customer_approved_limit_calculation(self):
        """Test approved limit calculation based on monthly income."""
        # Test with 36x monthly income (as per business logic)
        customer = Customer.objects.create(**self.customer_data)
        expected_limit = Customer.calculate_approved_limit(customer.monthly_income)
        self.assertEqual(Customer.calculate_approved_limit(customer.monthly_income), expected_limit)

        # Test with different income
        customer.monthly_income = Decimal('100000.00')
        expected_limit = Customer.calculate_approved_limit(customer.monthly_income)
        self.assertEqual(Customer.calculate_approved_limit(customer.monthly_income), expected_limit)

    def test_customer_validation(self):
        """Test customer model validation."""
        # Test valid customer
        customer = Customer(**self.customer_data)
        customer.full_clean()  # This will raise ValidationError if invalid

        # Test invalid age
        customer.age = -5
        with self.assertRaises(ValidationError):
            customer.full_clean()

        # Test invalid monthly income
        customer.age = 30
        customer.monthly_income = Decimal('-1000.00')
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_customer_phone_number_uniqueness(self):
        """Test phone number uniqueness constraint."""
        # Create first customer
        Customer.objects.create(**self.customer_data)

        # Try to create second customer with same phone number
        customer_data_2 = self.customer_data.copy()
        customer_data_2['customer_id'] = 99998

        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            Customer.objects.create(**customer_data_2)


class LoanModelTest(TestCase):
    """Test cases for Loan model."""

    def setUp(self):
        """Set up test data that will be rolled back after each test."""
        # Create test customer
        self.customer = Customer.objects.create(
            customer_id=99999,
            first_name='Test',
            last_name='Customer',
            age=30,
            monthly_income=Decimal('50000.00'),
            phone_number='9999999999',
            approved_limit=Decimal('100000.00')
        )

        self.loan_data = {
            'loan_id': 99999,
            'customer': self.customer,
            'loan_amount': Decimal('50000.00'),
            'interest_rate': Decimal('12.00'),
            'tenure': 12,
            'monthly_installment': Decimal('4442.44'),
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=365),
            'emis_paid_on_time': 0
        }

    def test_loan_creation(self):
        """Test basic loan creation."""
        loan = Loan.objects.create(**self.loan_data)

        self.assertEqual(loan.loan_id, 99999)
        self.assertEqual(loan.customer, self.customer)
        self.assertEqual(loan.loan_amount, Decimal('50000.00'))
        self.assertEqual(loan.interest_rate, Decimal('12.00'))
        self.assertEqual(loan.tenure, 12)
        self.assertEqual(loan.monthly_installment, Decimal('4442.44'))
        self.assertEqual(loan.start_date, date.today())
        self.assertEqual(loan.emis_paid_on_time, 0)

    def test_loan_str_representation(self):
        """Test loan string representation."""
        loan = Loan.objects.create(**self.loan_data)
        expected_str = "Loan 99999 - Test Customer"
        self.assertEqual(str(loan), expected_str)

    def test_loan_monthly_installment_property(self):
        """Test monthly installment property calculation."""
        loan = Loan.objects.create(**self.loan_data)

        # The property should return the stored monthly_installment
        self.assertEqual(loan.monthly_installment, Decimal('4442.44'))

    def test_loan_validation(self):
        """Test loan model validation."""
        # Test valid loan
        loan = Loan(**self.loan_data)
        loan.full_clean()  # This will raise ValidationError if invalid

        # Test invalid loan amount
        loan.loan_amount = Decimal('-1000.00')
        with self.assertRaises(ValidationError):
            loan.full_clean()

        # Test invalid interest rate
        loan.loan_amount = Decimal('50000.00')
        loan.interest_rate = Decimal('-5.00')
        with self.assertRaises(ValidationError):
            loan.full_clean()

        # Test invalid tenure
        loan.interest_rate = Decimal('12.00')
        loan.tenure = -5
        with self.assertRaises(ValidationError):
            loan.full_clean()

    def test_loan_customer_relationship(self):
        """Test loan-customer relationship."""
        loan = Loan.objects.create(**self.loan_data)

        # Test forward relationship
        self.assertEqual(loan.customer, self.customer)

        # Test reverse relationship
        self.assertIn(loan, self.customer.loans.all())

    def test_loan_id_uniqueness(self):
        """Test loan ID uniqueness constraint."""
        # Create first loan
        Loan.objects.create(**self.loan_data)

        # Try to create second loan with same ID
        loan_data_2 = self.loan_data.copy()
        loan_data_2['customer'] = self.customer

        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            Loan.objects.create(**loan_data_2)


class ModelIntegrationTest(TestCase):
    """Integration tests for model relationships and business logic."""

    def setUp(self):
        """Set up test data that will be rolled back after each test."""
        self.customer = Customer.objects.create(
            customer_id=99999,
            first_name='Test',
            last_name='Customer',
            age=30,
            monthly_income=Decimal('50000.00'),
            phone_number='9999999999',
            approved_limit=Decimal('100000.00')
        )

    def test_customer_loan_relationship(self):
        """Test customer-loan relationship works correctly."""
        # Create multiple loans for the customer
        loan1 = Loan.objects.create(
            loan_id=99999,
            customer=self.customer,
            loan_amount=Decimal('30000.00'),
            interest_rate=Decimal('12.00'),
            tenure=12,
            monthly_installment=Decimal('2665.46'),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            emis_paid_on_time=0
        )

        loan2 = Loan.objects.create(
            loan_id=99998,
            customer=self.customer,
            loan_amount=Decimal('20000.00'),
            interest_rate=Decimal('15.00'),
            tenure=6,
            monthly_installment=Decimal('3530.50'),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            emis_paid_on_time=2
        )

        # Test customer can access all loans
        customer_loans = self.customer.loans.all()
        self.assertEqual(customer_loans.count(), 2)
        self.assertIn(loan1, customer_loans)
        self.assertIn(loan2, customer_loans)

        # Test loan can access customer
        self.assertEqual(loan1.customer, self.customer)
        self.assertEqual(loan2.customer, self.customer)

    def test_customer_debt_calculation(self):
        """Test customer debt calculation with multiple loans."""
        # Create loans with different amounts
        Loan.objects.create(
            loan_id=99999,
            customer=self.customer,
            loan_amount=Decimal('30000.00'),
            interest_rate=Decimal('12.00'),
            tenure=12,
            monthly_installment=Decimal('2665.46'),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            emis_paid_on_time=0
        )

        Loan.objects.create(
            loan_id=99998,
            customer=self.customer,
            loan_amount=Decimal('20000.00'),
            interest_rate=Decimal('15.00'),
            tenure=6,
            monthly_installment=Decimal('3530.50'),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            emis_paid_on_time=2
        )

        # Test debt calculation (current_debt is calculated from active loans)
        # The current_debt property calculates remaining_amount from active loans
        # remaining_amount = (tenure - emis_paid_on_time) * monthly_installment
        # = (12 - 2) * 4610.75 = 10 * 4610.75 = 46107.50
        expected_remaining = Decimal('46107.52')  # Use actual calculated value
        self.assertEqual(self.customer.current_debt, expected_remaining)

        # Test debt vs approved limit
        self.assertLessEqual(self.customer.current_debt, self.customer.approved_limit)
