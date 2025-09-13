"""
Customer management service for the Credit Approval System.

This module handles customer registration and data management operations.
"""

import logging
from decimal import Decimal
from typing import Dict, Optional

from django.db import transaction

from ..models import Customer

logger = logging.getLogger(__name__)


class CustomerManagementService:
    """Service for managing customers and customer-related operations."""

    @staticmethod
    def register_customer(
        first_name: str,
        last_name: str,
        age: int,
        monthly_income: Decimal,
        phone_number: str,
        approved_limit: Decimal
    ) -> Dict:
        """
        Register a new customer.
        
        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            age: Customer's age
            monthly_income: Customer's monthly income
            phone_number: Customer's phone number
            approved_limit: Approved credit limit
            
        Returns:
            Dictionary with customer registration result
        """
        try:
            # Check if phone number already exists
            if Customer.objects.filter(phone_number=phone_number).exists():
                return {
                    'customer_id': None,
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'monthly_income': float(monthly_income),
                    'phone_number': phone_number,
                    'approved_limit': float(approved_limit),
                    'message': 'Phone number already exists'
                }
            
            # Generate customer ID (simple auto-increment for now)
            last_customer = Customer.objects.order_by('-customer_id').first()
            customer_id = (last_customer.customer_id + 1) if last_customer else 1
            
            with transaction.atomic():
                customer = Customer.objects.create(
                    customer_id=customer_id,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    monthly_income=monthly_income,
                    phone_number=phone_number,
                    approved_limit=approved_limit,
                )
                
                logger.info(f"Customer {customer_id} registered successfully")
                
                return {
                    'customer_id': customer.customer_id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'age': customer.age,
                    'monthly_income': float(customer.monthly_income),
                    'phone_number': customer.phone_number,
                    'approved_limit': float(customer.approved_limit),
                    'message': 'Customer registered successfully'
                }
                
        except Exception as e:
            logger.error(f"Error registering customer: {e}")
            return {
                'customer_id': None,
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'monthly_income': float(monthly_income),
                'phone_number': phone_number,
                'approved_limit': float(approved_limit),
                'message': f'Error registering customer: {str(e)}'
            }

    @staticmethod
    def get_customer_details(customer_id: int) -> Optional[Dict]:
        """
        Get detailed information about a specific customer.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            Dictionary with customer details or None if not found
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            return {
                'customer_id': customer.customer_id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'age': customer.age,
                'monthly_income': float(customer.monthly_income),
                'phone_number': customer.phone_number,
                'approved_limit': float(customer.approved_limit),
                'current_debt': float(customer.current_debt),
                'credit_utilization': float(customer.current_debt / customer.approved_limit * 100) if customer.approved_limit > 0 else 0
            }
        except Customer.DoesNotExist:
            return None

    @staticmethod
    def update_customer_debt(customer_id: int, debt_change: Decimal) -> bool:
        """
        Update customer's current debt.
        
        Note: current_debt is calculated from active loans, not stored directly.
        This method is kept for compatibility but doesn't actually modify stored debt.
        
        Args:
            customer_id: ID of the customer
            debt_change: Change in debt (positive for increase, negative for decrease)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            # Note: current_debt is calculated from active loans, not stored directly
            # The debt will be automatically calculated by the property
            logger.info(f"Customer {customer_id} found - debt is calculated from active loans")
            return True
        except Customer.DoesNotExist:
            logger.error(f"Customer {customer_id} not found for debt update")
            return False
        except Exception as e:
            logger.error(f"Error updating customer debt: {e}")
            return False
