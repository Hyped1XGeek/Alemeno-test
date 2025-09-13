#!/usr/bin/env python3
"""
Temporary script to debug credit score calculation for customer 316.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from credit_system.models import Customer, Loan
from credit_system.services.credit_scoring import CreditScoringService
from decimal import Decimal
from datetime import date

def main():
    print("🔍 Debugging Credit Score for Customer 316...")
    
    # Get customer 316
    customer = Customer.objects.get(customer_id=316)
    
    print(f"📊 Customer Details:")
    print(f"   Name: {customer.full_name}")
    print(f"   Age: {customer.age}")
    print(f"   Monthly Income: Rs.{customer.monthly_income}")
    print(f"   Approved Limit: Rs.{customer.approved_limit}")
    print(f"   Current Debt: Rs.{customer.current_debt}")
    
    # Get all loans for this customer
    all_loans = customer.loans.all()
    print(f"\n📋 Loan History:")
    print(f"   Total Loans: {all_loans.count()}")
    
    if all_loans.exists():
        for loan in all_loans:
            status = "Active" if loan.end_date >= date.today() else "Completed"
            print(f"   Loan {loan.loan_id}: Rs.{loan.loan_amount} @ {loan.interest_rate}%")
            print(f"     Tenure: {loan.tenure} months")
            print(f"     EMIs Paid: {loan.emis_paid_on_time}/{loan.tenure}")
            print(f"     Start: {loan.start_date}")
            print(f"     End: {loan.end_date}")
            print(f"     Status: {status}")
            print(f"     Monthly Installment: Rs.{loan.monthly_installment}")
            print()
    
    # Calculate credit score step by step
    print("🧮 Credit Score Calculation:")
    
    # Check if current debt exceeds approved limit
    if customer.current_debt > customer.approved_limit:
        print("   ❌ Current debt exceeds approved limit → Score = 0")
        return
    
    score = 0
    customer_loans = customer.loans.all()
    
    if not customer_loans.exists():
        print("   📝 No loan history → Default score = 50")
        return
    
    # Component 1: Past Loans paid on time (30 points)
    past_loans = customer_loans.filter(end_date__lt=date.today())
    total_past_loans = past_loans.count()
    print(f"   📅 Past Loans: {total_past_loans}")
    
    if total_past_loans > 0:
        paid_on_time = 0
        for loan in past_loans:
            if loan.emis_paid_on_time >= loan.tenure:
                paid_on_time += 1
        on_time_ratio = paid_on_time / total_past_loans if total_past_loans > 0 else 0
        component1_score = int(on_time_ratio * 30)
        score += component1_score
        print(f"   ✅ Component 1 (Past Loans Paid On Time): {component1_score}/30 points")
        print(f"      Loans paid on time: {paid_on_time}/{total_past_loans}")
    else:
        print(f"   ⚪ Component 1 (Past Loans Paid On Time): 0/30 points (no past loans)")
    
    # Component 2: Number of loans taken in past (15 points)
    loan_count = customer_loans.count()
    if loan_count >= 5:
        component2_score = 15
    elif loan_count >= 3:
        component2_score = 10
    elif loan_count >= 1:
        component2_score = 5
    else:
        component2_score = 0
    score += component2_score
    print(f"   📊 Component 2 (Number of Loans): {component2_score}/15 points")
    print(f"      Total loans: {loan_count}")
    
    # Component 3: Loan activity in current year (15 points)
    current_year = date.today().year
    current_year_loans = customer_loans.filter(start_date__year=current_year)
    current_year_count = current_year_loans.count()
    if current_year_count >= 2:
        component3_score = 15
    elif current_year_count >= 1:
        component3_score = 10
    else:
        component3_score = 0
    score += component3_score
    print(f"   📅 Component 3 (Current Year Activity): {component3_score}/15 points")
    print(f"      Current year loans: {current_year_count}")
    
    # Component 4: Loan approved volume (20 points)
    total_volume = sum(loan.loan_amount for loan in customer_loans)
    if total_volume >= Decimal('1000000'):  # 10 lakhs
        component4_score = 20
    elif total_volume >= Decimal('500000'):  # 5 lakhs
        component4_score = 15
    elif total_volume >= Decimal('100000'):  # 1 lakh
        component4_score = 10
    elif total_volume >= Decimal('10000'):   # 10k - give some points for small loans
        component4_score = 5
    else:
        component4_score = 0
    score += component4_score
    print(f"   💰 Component 4 (Loan Volume): {component4_score}/20 points")
    print(f"      Total volume: Rs.{total_volume}")
    
    final_score = min(score, 100)
    print(f"\n🎯 Final Credit Score: {final_score}/100")
    
    # Test loan approval
    print(f"\n🧪 Loan Approval Test:")
    approved, message, corrected_rate = CreditScoringService.check_loan_approval(
        customer,
        Decimal('1000.00'),
        Decimal('5.0'),
        48
    )
    print(f"   Result: {'✅ APPROVED' if approved else '❌ REJECTED'}")
    print(f"   Message: {message}")

if __name__ == "__main__":
    main()
