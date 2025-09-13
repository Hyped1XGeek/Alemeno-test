#!/usr/bin/env python3
"""
CSV Data Import Script for Credit Approval System.

This script allows you to import new CSV files for customers and loans.
It supports both customer_data.csv and loan_data.csv formats.
"""

import os
import sys
import pandas as pd
from decimal import Decimal
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from credit_system.models import Customer, Loan
from credit_system.logging_config import get_logger

logger = get_logger(__name__)


class CSVDataImporter:
    """Class to handle CSV data import operations."""
    
    def __init__(self):
        self.imported_customers = 0
        self.imported_loans = 0
        self.errors = []
    
    def import_customer_data(self, csv_file_path: str) -> bool:
        """
        Import customer data from CSV file.
        
        Expected CSV format:
        customer_id,first_name,last_name,age,monthly_income,phone_number,approved_limit
        
        Args:
            csv_file_path: Path to the customer CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Starting customer data import from: {csv_file_path}")
            
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            
            # Validate required columns
            required_columns = [
                'customer_id', 'first_name', 'last_name', 'age', 
                'monthly_income', 'phone_number', 'approved_limit'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                error_msg = f"Missing required columns: {missing_columns}"
                logger.error(error_msg)
                self.errors.append(error_msg)
                return False
            
            # Import customers
            for index, row in df.iterrows():
                try:
                    # Check if customer already exists
                    if Customer.objects.filter(customer_id=row['customer_id']).exists():
                        logger.warning(f"Customer {row['customer_id']} already exists, skipping")
                        continue
                    
                    # Create customer
                    customer = Customer.objects.create(
                        customer_id=int(row['customer_id']),
                        first_name=str(row['first_name']),
                        last_name=str(row['last_name']),
                        age=int(row['age']),
                        monthly_income=Decimal(str(row['monthly_income'])),
                        phone_number=str(row['phone_number']),
                        approved_limit=Decimal(str(row['approved_limit'])),
                        current_debt=Decimal('0')  # Default current debt
                    )
                    
                    self.imported_customers += 1
                    logger.info(f"Imported customer: {customer.customer_id} - {customer.first_name} {customer.last_name}")
                    
                except Exception as e:
                    error_msg = f"Error importing customer at row {index + 1}: {e}"
                    logger.error(error_msg)
                    self.errors.append(error_msg)
            
            logger.info(f"Customer import completed. Imported: {self.imported_customers} customers")
            return True
            
        except Exception as e:
            error_msg = f"Error reading customer CSV file: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False
    
    def import_loan_data(self, csv_file_path: str) -> bool:
        """
        Import loan data from CSV file.
        
        Expected CSV format:
        loan_id,customer_id,loan_amount,interest_rate,tenure,monthly_installment,start_date,end_date,emis_paid_on_time
        
        Args:
            csv_file_path: Path to the loan CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Starting loan data import from: {csv_file_path}")
            
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            
            # Validate required columns
            required_columns = [
                'loan_id', 'customer_id', 'loan_amount', 'interest_rate', 
                'tenure', 'monthly_installment', 'start_date', 'end_date', 'emis_paid_on_time'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                error_msg = f"Missing required columns: {missing_columns}"
                logger.error(error_msg)
                self.errors.append(error_msg)
                return False
            
            # Import loans
            for index, row in df.iterrows():
                try:
                    # Check if loan already exists
                    if Loan.objects.filter(loan_id=row['loan_id']).exists():
                        logger.warning(f"Loan {row['loan_id']} already exists, skipping")
                        continue
                    
                    # Get customer
                    try:
                        customer = Customer.objects.get(customer_id=row['customer_id'])
                    except Customer.DoesNotExist:
                        error_msg = f"Customer {row['customer_id']} not found for loan {row['loan_id']}"
                        logger.error(error_msg)
                        self.errors.append(error_msg)
                        continue
                    
                    # Parse dates
                    start_date = pd.to_datetime(row['start_date']).date()
                    end_date = pd.to_datetime(row['end_date']).date()
                    
                    # Create loan
                    loan = Loan.objects.create(
                        loan_id=int(row['loan_id']),
                        customer=customer,
                        loan_amount=Decimal(str(row['loan_amount'])),
                        interest_rate=Decimal(str(row['interest_rate'])),
                        tenure=int(row['tenure']),
                        monthly_installment=Decimal(str(row['monthly_installment'])),
                        start_date=start_date,
                        end_date=end_date,
                        emis_paid_on_time=int(row['emis_paid_on_time'])
                    )
                    
                    self.imported_loans += 1
                    logger.info(f"Imported loan: {loan.loan_id} for customer {customer.customer_id}")
                    
                except Exception as e:
                    error_msg = f"Error importing loan at row {index + 1}: {e}"
                    logger.error(error_msg)
                    self.errors.append(error_msg)
            
            logger.info(f"Loan import completed. Imported: {self.imported_loans} loans")
            return True
            
        except Exception as e:
            error_msg = f"Error reading loan CSV file: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False
    
    def print_summary(self):
        """Print import summary."""
        print("\n" + "="*60)
        print("📊 CSV IMPORT SUMMARY")
        print("="*60)
        print(f"✅ Customers imported: {self.imported_customers}")
        print(f"✅ Loans imported: {self.imported_loans}")
        print(f"❌ Errors encountered: {len(self.errors)}")
        
        if self.errors:
            print("\n🚨 ERRORS:")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        print("="*60)


def main():
    """Main function to handle CSV import."""
    print("📥 Credit Approval System - CSV Data Import")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("Usage: python import_csv_data.py <csv_file_path> [customer|loan]")
        print("\nExamples:")
        print("  python import_csv_data.py customer_data.csv customer")
        print("  python import_csv_data.py loan_data.csv loan")
        print("  python import_csv_data.py new_customers.csv customer")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    data_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if file exists
    if not os.path.exists(csv_file_path):
        print(f"❌ File not found: {csv_file_path}")
        sys.exit(1)
    
    # Initialize importer
    importer = CSVDataImporter()
    
    # Import data based on type
    if data_type == "customer" or "customer" in csv_file_path.lower():
        success = importer.import_customer_data(csv_file_path)
    elif data_type == "loan" or "loan" in csv_file_path.lower():
        success = importer.import_loan_data(csv_file_path)
    else:
        # Try to auto-detect based on filename
        if "customer" in csv_file_path.lower():
            success = importer.import_customer_data(csv_file_path)
        elif "loan" in csv_file_path.lower():
            success = importer.import_loan_data(csv_file_path)
        else:
            print("❌ Cannot determine data type. Please specify 'customer' or 'loan'")
            sys.exit(1)
    
    # Print summary
    importer.print_summary()
    
    if success and not importer.errors:
        print("🎉 Import completed successfully!")
        sys.exit(0)
    else:
        print("❌ Import completed with errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
