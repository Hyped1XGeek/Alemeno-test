"""
Django REST Framework serializers for the Credit Approval System.
"""

from decimal import Decimal
from rest_framework import serializers

from .models import Customer, Loan


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    
    name = serializers.CharField(source="full_name", read_only=True)
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "first_name",
            "last_name",
            "name",
            "age",
            "phone_number",
            "monthly_income",
            "approved_limit",
        ]
        read_only_fields = ["customer_id", "approved_limit"]


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model."""
    
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)
    start_date = serializers.DateField()
    
    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "customer",
            "loan_amount",
            "tenure",
            "interest_rate",
            "monthly_installment",
            "emis_paid_on_time",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["loan_id", "emis_paid_on_time"]


class RegisterRequestSerializer(serializers.Serializer):
    """Serializer for customer registration request."""
    
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=18, max_value=100)
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0'))
    phone_number = serializers.CharField(max_length=15)


class RegisterResponseSerializer(serializers.Serializer):
    """Serializer for customer registration response."""
    
    customer_id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    approved_limit = serializers.IntegerField()
    phone_number = serializers.CharField()


class CheckEligibilityRequestSerializer(serializers.Serializer):
    """Serializer for loan eligibility check request."""
    
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0'))
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=Decimal('0'))
    tenure = serializers.IntegerField(min_value=1, max_value=360)


class CheckEligibilityResponseSerializer(serializers.Serializer):
    """Serializer for loan eligibility check response."""
    
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)


class CreateLoanRequestSerializer(serializers.Serializer):
    """Serializer for loan creation request."""
    
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0'))
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=Decimal('0'))
    tenure = serializers.IntegerField(min_value=1, max_value=360)


class CreateLoanResponseSerializer(serializers.Serializer):
    """Serializer for loan creation response."""
    
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField()
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)


class ViewLoanResponseSerializer(serializers.Serializer):
    """Serializer for loan view response."""
    
    loan_id = serializers.IntegerField()
    customer = serializers.DictField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)
    tenure = serializers.IntegerField()


class ViewCustomerLoansResponseSerializer(serializers.Serializer):
    """Serializer for customer loans view response."""
    
    loan_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = serializers.DecimalField(max_digits=12, decimal_places=2)
    repayments_left = serializers.IntegerField()