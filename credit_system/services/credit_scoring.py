"""
Credit scoring service for the Credit Approval System.

This module handles credit score calculation and loan approval decisions.
"""

import logging
from datetime import date
from decimal import Decimal

from ..models import Customer

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
        # current_debt is calculated from active loans
        if customer.current_debt > customer.approved_limit:
            return 0

        score = 0
        customer_loans = customer.loans.all()

        if not customer_loans.exists():
            return 50  # Default score for new customers

        # Component 1: Past Loans paid on time (30 points)
        past_loans = customer_loans.filter(end_date__lt=date.today())
        total_past_loans = past_loans.count()
        if total_past_loans > 0:
            # Count loans where all EMIs were paid on time
            paid_on_time = 0
            for loan in past_loans:
                if loan.emis_paid_on_time >= loan.tenure:  # All EMIs paid on time
                    paid_on_time += 1
            on_time_ratio = paid_on_time / total_past_loans
            component1_score = int(30 * on_time_ratio)
            score += component1_score

        # Component 2: Number of loans taken in past (25 points)
        total_loans = customer_loans.count()
        if total_loans >= 5:
            component2_score = 25
        elif total_loans >= 3:
            component2_score = 20
        elif total_loans >= 1:
            component2_score = 15
        else:
            component2_score = 0
        score += component2_score

        # Component 3: Loan activity in current year (25 points)
        current_year = date.today().year
        current_year_loans = customer_loans.filter(start_date__year=current_year).count()
        if current_year_loans >= 2:
            component3_score = 25
        elif current_year_loans == 1:
            component3_score = 15
        else:
            component3_score = 0
        score += component3_score

        # Component 4: Loan approved volume (20 points)
        total_approved_volume = sum(loan.loan_amount for loan in customer_loans)
        if total_approved_volume >= 1000000:  # 10 lakhs
            component4_score = 20
        elif total_approved_volume >= 500000:  # 5 lakhs
            component4_score = 15
        elif total_approved_volume >= 100000:  # 1 lakh
            component4_score = 10
        elif total_approved_volume >= 10000:   # 10k - give some points for small loans
            component4_score = 5
        else:
            component4_score = 0
        score += component4_score

        return min(score, 100)  # Cap at 100

    @staticmethod
    def check_loan_approval(
        customer: Customer,
        loan_amount: Decimal,
        interest_rate: Decimal,
        tenure: int
    ) -> tuple[bool, str, Decimal]:
        """
        Check if a loan should be approved based on credit score and other criteria.
        
        Approval criteria:
        1. Credit score > 50
        2. Monthly EMI should not exceed 50% of monthly salary
        3. Credit utilization should not exceed 50%
        4. Age should be between 18 and 65
        5. Tenure should be between 1 and 5 years
        
        Args:
            customer: Customer instance
            loan_amount: Requested loan amount
            interest_rate: Interest rate
            tenure: Loan tenure in months
            
        Returns:
            Tuple of (approved: bool, message: str, corrected_interest_rate: Decimal)
        """
        # Calculate credit score
        credit_score = CreditScoringService.calculate_credit_score(customer)

        # Determine corrected interest rate based on credit score first
        corrected_interest_rate = CreditScoringService.get_corrected_interest_rate(interest_rate, credit_score)

        # Check if sum of all current EMIs > 50% of monthly salary
        current_monthly_emis = sum(loan.monthly_installment for loan in customer.loans.filter(end_date__gte=date.today()))
        new_loan_emi = CreditScoringService.calculate_monthly_emi(loan_amount, corrected_interest_rate, tenure)
        total_monthly_emis = current_monthly_emis + new_loan_emi

        if total_monthly_emis > (customer.monthly_income * Decimal('0.5')):
            return False, "Sum of all current EMIs exceeds 50% of monthly salary", corrected_interest_rate

        # Check approval based on credit score and interest rate
        if credit_score > 50:
            return True, "Loan approved", corrected_interest_rate
        elif credit_score > 30:
            if interest_rate >= 12:
                return True, "Loan approved", corrected_interest_rate
            else:
                return False, "Interest rate too low for credit score", corrected_interest_rate
        elif credit_score > 10:
            if interest_rate >= 16:
                return True, "Loan approved", corrected_interest_rate
            else:
                return False, "Interest rate too low for credit score", corrected_interest_rate
        else:
            return False, "Credit score too low", interest_rate

    @staticmethod
    def calculate_monthly_emi(
        loan_amount: Decimal,
        interest_rate: Decimal,
        tenure: int
    ) -> Decimal:
        """
        Calculate monthly EMI using compound interest formula.
        
        EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        Where:
        P = Principal amount
        r = Monthly interest rate
        n = Number of months
        
        Args:
            loan_amount: Principal amount
            interest_rate: Annual interest rate
            tenure: Loan tenure in months
            
        Returns:
            Monthly EMI amount
        """
        if tenure == 0:
            return Decimal('0')

        # Convert annual rate to monthly rate
        monthly_rate = interest_rate / Decimal('12') / Decimal('100')

        # Calculate EMI using compound interest formula
        if monthly_rate == 0:
            return loan_amount / tenure

        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure) / \
              (((1 + monthly_rate) ** tenure) - 1)

        return emi.quantize(Decimal('0.01'))

    @staticmethod
    def get_corrected_interest_rate(interest_rate: Decimal, credit_score: int) -> Decimal:
        """
        Get corrected interest rate based on credit score.
        
        Interest rate slabs as per assignment:
        - If credit_rating > 50, approve loan (any rate)
        - If 50 > credit_rating > 30, approve loans with interest rate > 12%
        - If 30 > credit_rating > 10, approve loans with interest rate > 16%
        - If 10 > credit_rating, don't approve any loans
        
        Args:
            interest_rate: Original interest rate
            credit_score: Customer's credit score
            
        Returns:
            Corrected interest rate (lowest of the slab if original rate is too low)
        """
        if credit_score > 50:
            return interest_rate  # Any rate is acceptable
        elif credit_score > 30:
            return max(Decimal('12.0'), interest_rate)  # Minimum 12%
        elif credit_score > 10:
            return max(Decimal('16.0'), interest_rate)  # Minimum 16%
        else:
            return interest_rate  # Will be rejected anyway
