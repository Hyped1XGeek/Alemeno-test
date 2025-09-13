"""
Django models for the Credit Approval System.

This module contains the Customer and Loan models that represent the core entities in the credit approval system.
"""

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Customer(models.Model):
    """
    Customer model representing a customer in the credit system.
    
    Attributes:
        customer_id: Unique identifier for the customer
        first_name: Customer's first name
        last_name: Customer's last name
        age: Customer's age
        phone_number: Customer's phone number
        monthly_salary: Customer's monthly salary
        approved_limit: Maximum credit limit approved for the customer
        created_at: Timestamp when the customer was created
        updated_at: Timestamp when the customer was last updated
    """

    customer_id = models.PositiveIntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_income = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    approved_limit = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Customer model."""

        db_table = "customers"
        ordering = ["customer_id"]

    def __str__(self):
        """String representation of the Customer model."""
        return f"{self.first_name} {self.last_name} (ID: {self.customer_id})"

    @property
    def full_name(self):
        """Return the full name of the customer."""
        return f"{self.first_name} {self.last_name}"

    @property
    def current_debt(self):
        """Calculate the current debt of the customer."""
        from datetime import date
        active_loans = self.loans.filter(end_date__gt=date.today())
        return sum(loan.remaining_amount for loan in active_loans)

    @property
    def credit_utilization_ratio(self):
        """Calculate the credit utilization ratio."""
        if self.approved_limit == 0:
            return Decimal('0')
        return (self.current_debt / self.approved_limit) * 100

    @classmethod
    def calculate_approved_limit(cls, monthly_income):
        """Calculate approved limit based on monthly income."""
        # approved_limit = 36 * monthly_salary (rounded to nearest lakh)
        base_limit = monthly_income * 36
        # Round to nearest lakh (100000)
        lakh = Decimal('100000')
        # Use round() to properly round to nearest lakh
        lakhs = round(base_limit / lakh)
        return lakhs * lakh


class Loan(models.Model):
    """
    Loan model representing a loan in the credit system.
    
    Attributes:
        loan_id: Unique identifier for the loan
        customer: Foreign key to the Customer model
        loan_amount: Amount of the loan
        tenure: Loan tenure in months
        interest_rate: Interest rate for the loan
        monthly_payment: Monthly payment amount
        emis_paid_on_time: Number of EMIs paid on time
        date_of_approval: Date when the loan was approved
        end_date: End date of the loan
        created_at: Timestamp when the loan was created
        updated_at: Timestamp when the loan was last updated
    """

    loan_id = models.PositiveIntegerField(unique=True, primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="loans"
    )
    loan_amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    tenure = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(360)]
    )
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    monthly_installment = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    emis_paid_on_time = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Loan model."""

        db_table = "loans"
        ordering = ["-start_date"]

    def __str__(self):
        """String representation of the Loan model."""
        return f"Loan {self.loan_id} - {self.customer.full_name}"

    @property
    def is_active(self):
        """Check if the loan is currently active."""
        from datetime import date
        return self.end_date > date.today()

    @property
    def total_paid(self):
        """Calculate the total amount paid so far."""
        return self.emis_paid_on_time * self.monthly_installment

    @property
    def remaining_amount(self):
        """Calculate the remaining loan amount."""
        if not self.is_active:
            return Decimal('0')

        total_emis = self.tenure
        remaining_emis = total_emis - self.emis_paid_on_time
        return remaining_emis * self.monthly_installment

    @property
    def repayments_left(self):
        """Calculate the number of EMIs left."""
        if not self.is_active:
            return 0
        return self.tenure - self.emis_paid_on_time

    @property
    def payment_history_score(self):
        """Calculate payment history score based on on-time payments."""
        if self.tenure == 0:
            return 0
        return (self.emis_paid_on_time / self.tenure) * 100
