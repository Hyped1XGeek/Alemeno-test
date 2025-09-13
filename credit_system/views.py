"""
Django REST Framework views for the Credit Approval System.

This module contains API views that match the assignment requirements exactly.
"""

import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer
from .services import (
    CreditScoringService,
    CustomerManagementService,
    LoanManagementService,
)

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new customer.
    
    POST /register
    """
    try:
        # Validate required fields
        required_fields = ["first_name", "last_name", "age", "monthly_income", "phone_number"]
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {"error": f"Missing required field: {field}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate data types
        try:
            age = int(request.data["age"])
            monthly_income = Decimal(str(request.data["monthly_income"]))
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid data types for age or monthly_income"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if phone number already exists
        if Customer.objects.filter(phone_number=request.data["phone_number"]).exists():
            return Response(
                {"error": "Phone number already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate approved limit based on monthly income
        approved_limit = Customer.calculate_approved_limit(monthly_income)

        # Register customer
        result = CustomerManagementService.register_customer(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            age=age,
            monthly_income=monthly_income,
            phone_number=request.data["phone_number"],
            approved_limit=approved_limit
        )

        return Response(result, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error in register: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_eligibility(request):
    """
    Check loan eligibility for a customer.
    
    POST /check-eligibility
    """
    try:
        # Validate required fields
        required_fields = ["customer_id", "loan_amount", "interest_rate", "tenure"]
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {"error": f"Missing required field: {field}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate data types
        try:
            customer_id = int(request.data["customer_id"])
            loan_amount = Decimal(str(request.data["loan_amount"]))
            interest_rate = Decimal(str(request.data["interest_rate"]))
            tenure = int(request.data["tenure"])
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid data types"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get customer and check eligibility
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check loan approval
        approved, message, corrected_interest_rate = CreditScoringService.check_loan_approval(
            customer, loan_amount, interest_rate, tenure
        )

        # Calculate monthly installment
        monthly_installment = CreditScoringService.calculate_monthly_emi(
            loan_amount, corrected_interest_rate, tenure
        )

        result = {
            'customer_id': customer_id,
            'approval': approved,
            'interest_rate': float(interest_rate),
            'corrected_interest_rate': float(corrected_interest_rate),
            'tenure': tenure,
            'monthly_installment': float(monthly_installment)
        }

        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in check_eligibility: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_loan(request):
    """
    Create a new loan for a customer.
    
    POST /create-loan
    """
    try:
        # Validate required fields
        required_fields = ["customer_id", "loan_amount", "interest_rate", "tenure"]
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {"error": f"Missing required field: {field}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate data types
        try:
            customer_id = int(request.data["customer_id"])
            loan_amount = Decimal(str(request.data["loan_amount"]))
            interest_rate = Decimal(str(request.data["interest_rate"]))
            tenure = int(request.data["tenure"])
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid data types"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create loan
        result = LoanManagementService.create_loan(
            customer_id=customer_id,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure=tenure,
        )

        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        # Return appropriate status code based on approval
        status_code = status.HTTP_201_CREATED if result["loan_approved"] else status.HTTP_400_BAD_REQUEST

        return Response(result, status=status_code)

    except Exception as e:
        logger.error(f"Error in create_loan: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def view_loan(request, loan_id):
    """
    View loan details and customer details.
    
    GET /view-loan/{loan_id}
    """
    try:
        loan_id = int(loan_id)
    except ValueError:
        return Response(
            {"error": "Invalid loan ID"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = LoanManagementService.get_loan_details(loan_id)

        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in view_loan: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def view_customer_loans(request, customer_id):
    """
    View all current loan details by customer ID.
    
    GET /view-loans/{customer_id}
    """
    try:
        customer_id = int(customer_id)
    except ValueError:
        return Response(
            {"error": "Invalid customer ID"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = LoanManagementService.get_customer_loans(customer_id)

        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in view_customer_loans: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Additional endpoints for system management (not in assignment but useful)
@api_view(["GET"])
@permission_classes([AllowAny])
def system_stats(request):
    """
    Get system statistics.
    
    GET /stats/
    """
    try:
        result = LoanManagementService.get_system_stats()
        return Response(result)

    except Exception as e:
        logger.error(f"Error in system_stats: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_credit_score(request, customer_id):
    """
    Get the credit score for a specific customer.
    
    Args:
        customer_id: ID of the customer
        
    Returns:
        JSON response with customer details and credit score
    """
    try:
        # Get customer
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Calculate credit score
        credit_score = CreditScoringService.calculate_credit_score(customer)

        # Prepare response
        result = {
            "customer_id": customer.customer_id,
            "name": customer.full_name,
            "age": customer.age,
            "monthly_income": float(customer.monthly_income),
            "approved_limit": float(customer.approved_limit),
            "current_debt": float(customer.current_debt),
            "credit_score": credit_score,
            "credit_utilization": float(customer.credit_utilization_ratio)
        }

        return Response(result)

    except Exception as e:
        logger.error(f"Error in get_credit_score: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
