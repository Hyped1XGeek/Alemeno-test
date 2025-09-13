"""
Django admin configuration for the Credit Approval System.

This module configures the Django admin interface for managing customers and loans.
"""

from django.contrib import admin
from .models import Customer, Loan


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin configuration for Customer model."""
    
    list_display = [
        "customer_id",
        "first_name",
        "last_name",
        "age",
        "phone_number",
        "monthly_income",
        "approved_limit",
        "created_at",
    ]
    list_filter = ["age", "created_at"]
    search_fields = ["first_name", "last_name", "phone_number", "customer_id"]
    readonly_fields = ["customer_id", "created_at", "updated_at"]
    ordering = ["customer_id"]


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Admin configuration for Loan model."""
    
    list_display = [
        "loan_id",
        "customer",
        "loan_amount",
        "tenure",
        "interest_rate",
        "monthly_installment",
        "start_date",
        "end_date",
        "is_active",
    ]
    list_filter = ["start_date", "end_date", "interest_rate"]
    search_fields = ["loan_id", "customer__first_name", "customer__last_name"]
    readonly_fields = ["loan_id", "created_at", "updated_at"]
    ordering = ["-start_date"]
