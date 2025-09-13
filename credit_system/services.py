"""
Business logic services for the Credit Approval System.

This module contains the core business logic for credit approval, credit scoring, and loan calculations according to assignment requirements.
"""

import logging
from decimal import Decimal
from typing import Dict, List, Tuple
from datetime import date, datetime

from django.db import transaction
from django.utils import timezone

from .models import Customer, Loan

logger = logging.getLogger(__name__)


class CreditScoringService:
    """Service for calculating credit scores (0-100 scale) and approval decisions."""

    @staticmethod
    def calculate_credit_score(customer: Customer) -> int:
        """
        Calculate credit score for a customer based on historical loan data.
        Score is out of 100.
        
        Components:
        i. Past Loans paid on time
        ii. No of loans taken in past
        iii. Loan activity in current year
        iv. Loan approved volume
        v. If sum of current loans > approved limit, credit score = 0
        
        Args:
            customer: Customer instance
            
        Returns:
            Credit score between 0 and 100
        """
        # Check if current debt exceeds approved limit
        if customer.current_debt > customer.approved_limit:
            return 0
        
        score = 0
        customer_loans = customer.loans.all()
        
        if not customer_loans.exists():
            return 50  # Default score for new customers
        
        # i. Past Loans paid on time (40 points max)
        total_emis = sum(loan.tenure for loan in customer_loans)
        total_paid_on_time = sum(loan.emis_paid_on_time for loan in customer_loans)
        
        if total_emis > 0:
            on_time_ratio = total_paid_on_time / total_emis
            score += int(on_time_ratio * 40)
        
        # ii. No of loans taken in past (20 points max)
        loan_count = customer_loans.count()
        if loan_count >= 5:
            score += 20
        elif loan_count >= 3:
            score += 15
        elif loan_count >= 1:
            score += 10
        
        # iii. Loan activity in current year (20 points max)
        current_year = date.today().year
        current_year_loans = customer_loans.filter(start_date__year=current_year)
        if current_year_loans.exists():
            score += 20
        
        # iv. Loan approved volume (20 points max)
        total_loan_volume = sum(loan.loan_amount for loan in customer_loans)
        if total_loan_volume >= 1000000:  # 10 lakhs
            score += 20
        elif total_loan_volume >= 500000:  # 5 lakhs
            score += 15
        elif total_loan_volume >= 100000:  # 1 lakh
            score += 10
        
        return min(100, max(0, score))

    @staticmethod
    def get_interest_rate_slab(credit_score: int) -> float:
        """
        Get the minimum interest rate based on credit score.
        
        Args:
            credit_score: Credit score (0-100)
            
        Returns:
            Minimum interest rate for the credit score
        """
        if credit_score > 50:
            return 12.0  # Can approve any rate >= 12%
        elif credit_score > 30:
            return 12.0  # Must be >= 12%
        elif credit_score > 10:
            return 16.0  # Must be >= 16%
        else:
            return 100.0  # No approval

    @staticmethod
    def should_approve_loan(
        customer: Customer, loan_amount: Decimal, tenure: int, interest_rate: Decimal
    ) -> Tuple[bool, List[str], float]:
        """
        Determine if a loan should be approved for a customer.
        
        Args:
            customer: Customer instance
            loan_amount: Requested loan amount
            tenure: Loan tenure in months
            interest_rate: Interest rate percentage
            
        Returns:
            Tuple of (approved: bool, reasons: List[str], corrected_interest_rate: float)
        """
        reasons = []
        approved = True
        
        # Check if customer exists
        if not customer:
            return False, ["Customer not found"], interest_rate
        
        # Calculate credit score
        credit_score = CreditScoringService.calculate_credit_score(customer)
        
        # Check if sum of current EMIs > 50% of monthly salary
        current_emis = sum(loan.monthly_installment for loan in customer.loans.filter(end_date__gt=date.today()))
        new_emi = LoanCalculationService.calculate_monthly_installment(loan_amount, tenure, interest_rate)
        total_emis = current_emis + new_emi
        
        if total_emis > customer.monthly_income * Decimal('0.5'):
            approved = False
            reasons.append("Sum of all current EMIs > 50% of monthly salary")
        
        # Check credit score and interest rate requirements
        min_interest_rate = CreditScoringService.get_interest_rate_slab(credit_score)
        
        if credit_score <= 10:
            approved = False
            reasons.append("Credit score too low (<= 10)")
        elif interest_rate < min_interest_rate:
            approved = False
            reasons.append(f"Interest rate too low. Minimum required: {min_interest_rate}%")
        
        # Calculate corrected interest rate
        corrected_interest_rate = max(interest_rate, min_interest_rate)
        
        if approved:
            reasons.append("Loan approved based on all criteria")
        
        return approved, reasons, float(corrected_interest_rate)


class LoanCalculationService:
    """Service for loan calculations using compound interest."""

    @staticmethod
    def calculate_monthly_installment(
        principal: Decimal, tenure_months: int, annual_rate: Decimal
    ) -> Decimal:
        """
        Calculate monthly installment using compound interest formula.
        
        Args:
            principal: Loan amount
            tenure_months: Loan tenure in months
            annual_rate: Annual interest rate as percentage
            
        Returns:
            Monthly installment amount
        """
        if tenure_months == 0:
            return Decimal('0')
        
        monthly_rate = annual_rate / 100 / 12
        
        if monthly_rate == 0:
            return principal / tenure_months
        
        # Compound interest formula for EMI
        monthly_installment = principal * (
            monthly_rate * (1 + monthly_rate) ** tenure_months
        ) / ((1 + monthly_rate) ** tenure_months - 1)
        
        return monthly_installment.quantize(Decimal('0.01'))


class CreditApprovalService:
    """Main service for credit approval operations."""

    @staticmethod
    def register_customer(
        first_name: str,
        last_name: str,
        age: int,
        monthly_income: Decimal,
        phone_number: str,
    ) -> Dict:
        """
        Register a new customer with calculated approved limit.
        
        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            age: Customer's age
            monthly_income: Monthly income
            phone_number: Phone number
            
        Returns:
            Dictionary containing customer details
        """
        # Calculate approved limit: 36 * monthly_salary (rounded to nearest lakh)
        approved_limit = Customer.calculate_approved_limit(monthly_income)
        
        # Get next customer ID
        last_customer = Customer.objects.order_by('-customer_id').first()
        customer_id = (last_customer.customer_id + 1) if last_customer else 1
        
        customer = Customer.objects.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            monthly_income=monthly_income,
            phone_number=phone_number,
            approved_limit=approved_limit,
        )
        
        return {
            "customer_id": customer.customer_id,
            "name": customer.full_name,
            "age": customer.age,
            "monthly_income": float(customer.monthly_income),
            "approved_limit": int(customer.approved_limit),
            "phone_number": customer.phone_number,
        }

    @staticmethod
    def check_eligibility(
        customer_id: int,
        loan_amount: Decimal,
        interest_rate: Decimal,
        tenure: int,
    ) -> Dict:
        """
        Check loan eligibility for a customer.
        
        Args:
            customer_id: Customer ID
            loan_amount: Requested loan amount
            interest_rate: Interest rate percentage
            tenure: Loan tenure in months
            
        Returns:
            Dictionary containing eligibility result
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return {"error": "Customer not found"}
        
        # Calculate monthly installment
        monthly_installment = LoanCalculationService.calculate_monthly_installment(
            loan_amount, tenure, interest_rate
        )
        
        # Check approval
        approved, reasons, corrected_interest_rate = CreditScoringService.should_approve_loan(
            customer, loan_amount, tenure, interest_rate
        )
        
        return {
            "customer_id": customer_id,
            "approval": approved,
            "interest_rate": float(interest_rate),
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": float(monthly_installment),
        }

    @staticmethod
    @transaction.atomic
    def create_loan(
        customer_id: int,
        loan_amount: Decimal,
        interest_rate: Decimal,
        tenure: int,
    ) -> Dict:
        """
        Create a new loan for a customer.
        
        Args:
            customer_id: Customer ID
            loan_amount: Requested loan amount
            interest_rate: Interest rate percentage
            tenure: Loan tenure in months
            
        Returns:
            Dictionary containing loan creation result
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return {"error": "Customer not found"}
        
        # Calculate monthly installment
        monthly_installment = LoanCalculationService.calculate_monthly_installment(
            loan_amount, tenure, interest_rate
        )
        
        # Check approval
        approved, reasons, corrected_interest_rate = CreditScoringService.should_approve_loan(
            customer, loan_amount, tenure, interest_rate
        )
        
        if approved:
            # Get next loan ID
            last_loan = Loan.objects.order_by('-loan_id').first()
            loan_id = (last_loan.loan_id + 1) if last_loan else 1
            
            # Create loan
            loan = Loan.objects.create(
                loan_id=loan_id,
                customer=customer,
                loan_amount=loan_amount,
                tenure=tenure,
                interest_rate=corrected_interest_rate,
                monthly_installment=monthly_installment,
                start_date=date.today(),
                end_date=date.today() + timezone.timedelta(days=tenure * 30),
            )
            
            return {
                "loan_id": loan.loan_id,
                "customer_id": customer_id,
                "loan_approved": True,
                "message": "Loan approved successfully",
                "monthly_installment": float(monthly_installment)
            }
        else:
            return {
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "; ".join(reasons),
                "monthly_installment": float(monthly_installment)
            }

    @staticmethod
    def view_loan(loan_id: int) -> Dict:
        """
        View loan details and customer details.
        
        Args:
            loan_id: Loan ID
            
        Returns:
            Dictionary containing loan and customer details
        """
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return {"error": "Loan not found"}
        
        return {
            "loan_id": loan.loan_id,
            "customer": {
                "id": loan.customer.customer_id,
                "first_name": loan.customer.first_name,
                "last_name": loan.customer.last_name,
                "phone_number": loan.customer.phone_number,
                "age": loan.customer.age,
            },
            "loan_amount": float(loan.loan_amount),
            "interest_rate": float(loan.interest_rate),
            "monthly_installment": float(loan.monthly_installment),
            "tenure": loan.tenure,
        }

    @staticmethod
    def view_customer_loans(customer_id: int) -> Dict:
        """
        View all current loan details by customer ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Dictionary with customer info and loan details
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return {"error": "Customer not found"}
        
        active_loans = customer.loans.filter(end_date__gt=date.today())
        
        loans = []
        for loan in active_loans:
            loans.append({
                "loan_id": loan.loan_id,
                "loan_amount": float(loan.loan_amount),
                "interest_rate": float(loan.interest_rate),
                "monthly_installment": float(loan.monthly_installment),
                "repayments_left": loan.repayments_left,
            })
        
        return {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "loans": loans
        }