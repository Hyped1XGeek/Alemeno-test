"""
Services package for Credit Approval System.

This package contains the business logic services split into different modules:
- credit_scoring: Credit score calculation and approval logic
- loan_management: Loan creation, viewing, and management
- customer_management: Customer registration and data management
"""

from .credit_scoring import CreditScoringService
from .loan_management import LoanManagementService
from .customer_management import CustomerManagementService

__all__ = [
    'CreditScoringService',
    'LoanManagementService', 
    'CustomerManagementService'
]
