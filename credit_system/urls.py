"""
URL configuration for the Credit Approval System.

This module defines the URL patterns that match the assignment requirements exactly.
"""

from django.urls import path

from . import views

app_name = "credit_system"

urlpatterns = [
    # Assignment required endpoints
    path("register/", views.register, name="register"),
    path("check-eligibility/", views.check_eligibility, name="check_eligibility"),
    path("create-loan/", views.create_loan, name="create_loan"),
    path("view-loan/<int:loan_id>/", views.view_loan, name="view_loan"),
    path("view-loans/<int:customer_id>/", views.view_customer_loans, name="view_customer_loans"),

    # Additional system management endpoints
    path("stats/", views.system_stats, name="system_stats"),
    path("credit-score/<int:customer_id>/", views.get_credit_score, name="get_credit_score"),
]
