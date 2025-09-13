"""
Loan management service for the Credit Approval System.

This module handles loan creation, viewing, and management operations.
"""

import logging
from datetime import date
from decimal import Decimal

from django.db import models, transaction

from ..models import Customer, Loan
from .credit_scoring import CreditScoringService

logger = logging.getLogger(__name__)


class LoanManagementService:
    """Service for managing loans and loan-related operations."""

    @staticmethod
    def create_loan(
        customer_id: int,
        loan_amount: Decimal,
        interest_rate: Decimal,
        tenure: int
    ) -> dict:
        """
        Create a new loan for a customer.
        
        Args:
            customer_id: ID of the customer
            loan_amount: Loan amount requested
            interest_rate: Interest rate
            tenure: Loan tenure in months
            
        Returns:
            Dictionary with loan creation result
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': 'Customer not found',
                'monthly_installment': None
            }

        try:
            # Check loan approval
            approved, message, corrected_interest_rate = CreditScoringService.check_loan_approval(
                customer, loan_amount, interest_rate, tenure
            )

            if not approved:
                return {
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': message,
                    'monthly_installment': None
                }

            # Calculate monthly installment
            monthly_installment = CreditScoringService.calculate_monthly_emi(
                loan_amount, corrected_interest_rate, tenure
            )

            # Create loan
            with transaction.atomic():
                # Generate unique loan_id
                max_loan_id = Loan.objects.aggregate(max_id=models.Max('loan_id'))['max_id']
                loan_id = (max_loan_id or 0) + 1

                loan = Loan.objects.create(
                    loan_id=loan_id,
                    customer=customer,
                    loan_amount=loan_amount,
                    interest_rate=corrected_interest_rate,
                    tenure=tenure,
                    monthly_installment=monthly_installment,
                    start_date=date.today(),
                    end_date=date.today().replace(
                        year=date.today().year + (tenure // 12),
                        month=date.today().month + (tenure % 12)
                    )
                )

                # Note: current_debt is calculated from active loans, not stored directly
                # The debt will be automatically calculated by the property

                logger.info(f"Loan {loan.loan_id} created for customer {customer_id}")

                return {
                    'loan_id': loan.loan_id,
                    'customer_id': customer_id,
                    'loan_approved': True,
                    'message': message,
                    'monthly_installment': float(monthly_installment)
                }

        except Exception as e:
            logger.error(f"Error creating loan: {e}")
            return {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': f'Error creating loan: {str(e)}',
                'monthly_installment': None
            }

    @staticmethod
    def get_loan_details(loan_id: int) -> dict | None:
        """
        Get detailed information about a specific loan.
        
        Args:
            loan_id: ID of the loan
            
        Returns:
            Dictionary with loan details or None if not found
        """
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            return {
                'loan_id': loan.loan_id,
                'customer': {
                    'id': loan.customer.customer_id,
                    'first_name': loan.customer.first_name,
                    'last_name': loan.customer.last_name,
                    'phone_number': loan.customer.phone_number,
                    'age': loan.customer.age
                },
                'loan_amount': float(loan.loan_amount),
                'interest_rate': float(loan.interest_rate),
                'monthly_installment': float(loan.monthly_installment),
                'tenure': loan.tenure
            }
        except Loan.DoesNotExist:
            return {"error": "Loan not found"}

    @staticmethod
    def get_customer_loans(customer_id: int) -> dict | None:
        """
        Get all loans for a specific customer.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            Dictionary with customer info and loans list, or None if customer not found
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            loans = customer.loans.all().order_by('-start_date')

            loans_data = []
            for loan in loans:
                loans_data.append({
                    'loan_id': loan.loan_id,
                    'loan_amount': float(loan.loan_amount),
                    'interest_rate': float(loan.interest_rate),
                    'monthly_installment': float(loan.monthly_installment),
                    'repayments_left': loan.tenure - loan.emis_paid_on_time,
                    'status': 'Active' if loan.end_date > date.today() else 'Completed'
                })

            return loans_data
        except Customer.DoesNotExist:
            return {"error": "Customer not found"}

    @staticmethod
    def get_system_stats() -> dict:
        """
        Get system-wide statistics.
        
        Returns:
            Dictionary with system statistics
        """
        total_customers = Customer.objects.count()
        total_loans = Loan.objects.count()
        active_loans = Loan.objects.filter(end_date__gt=date.today()).count()
        total_loan_amount = sum(loan.loan_amount for loan in Loan.objects.all())

        return {
            'total_customers': total_customers,
            'total_loans': total_loans,
            'active_loans': active_loans,
            'total_loan_amount': float(total_loan_amount)
        }
