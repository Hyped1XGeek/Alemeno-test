"""
Django management command to import customer and loan data from CSV files.

This command imports data from the provided CSV files into the database.
"""

import csv
import logging
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from credit_system.models import Customer, Loan

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Management command to import CSV data."""

    help = "Import customer and loan data from CSV files"

    def add_arguments(self, parser):
        """Add command line arguments."""
        parser.add_argument(
            "--customer-file",
            type=str,
            help="Path to customer CSV file",
            default="Docs/customer_data.csv",
        )
        parser.add_argument(
            "--loan-file",
            type=str,
            help="Path to loan CSV file",
            default="Docs/loan_data.csv",
        )
        parser.add_argument(
            "--clear-data",
            action="store_true",
            help="Clear existing data before importing",
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        customer_file = options["customer_file"]
        loan_file = options["loan_file"]
        clear_data = options["clear_data"]

        try:
            if clear_data:
                self.stdout.write("Clearing existing data...")
                Loan.objects.all().delete()
                Customer.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS("Existing data cleared successfully")
                )

            # Import customers
            self.stdout.write("Importing customers...")
            self.import_customers(customer_file)

            # Import loans
            self.stdout.write("Importing loans...")
            self.import_loans(loan_file)

            self.stdout.write(
                self.style.SUCCESS("Data import completed successfully!")
            )

        except Exception as e:
            raise CommandError(f"Error importing data: {str(e)}")

    def import_customers(self, file_path):
        """Import customer data from CSV file."""
        try:
            with open(file_path, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                customers_created = 0

                with transaction.atomic():
                    for row in reader:
                        customer_id = int(row["Customer ID"])

                        # Skip if customer already exists
                        if Customer.objects.filter(customer_id=customer_id).exists():
                            continue

                        customer = Customer.objects.create(
                            customer_id=customer_id,
                            first_name=row["First Name"],
                            last_name=row["Last Name"],
                            age=int(row["Age"]),
                            phone_number=row["Phone Number"],
                            monthly_income=Decimal(row["Monthly Salary"]),
                            approved_limit=Decimal(row["Approved Limit"]),
                        )
                        customers_created += 1

                self.stdout.write(
                    f"Created {customers_created} customers"
                )

        except FileNotFoundError:
            raise CommandError(f"Customer file not found: {file_path}")
        except Exception as e:
            raise CommandError(f"Error importing customers: {str(e)}")

    def import_loans(self, file_path):
        """Import loan data from CSV file."""
        try:
            with open(file_path, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                loans_created = 0

                with transaction.atomic():
                    for row in reader:
                        loan_id = int(row["Loan ID"])
                        customer_id = int(row["Customer ID"])

                        # Skip if loan already exists
                        if Loan.objects.filter(loan_id=loan_id).exists():
                            continue

                        try:
                            customer = Customer.objects.get(customer_id=customer_id)
                        except Customer.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Customer {customer_id} not found for loan {loan_id}"
                                )
                            )
                            continue

                        # Parse dates
                        from datetime import datetime
                        date_of_approval = datetime.strptime(
                            row["Date of Approval"], "%m/%d/%Y"
                        ).date()
                        end_date = datetime.strptime(
                            row["End Date"], "%m/%d/%Y"
                        ).date()

                        loan = Loan.objects.create(
                            loan_id=loan_id,
                            customer=customer,
                            loan_amount=Decimal(row["Loan Amount"]),
                            tenure=int(row["Tenure"]),
                            interest_rate=Decimal(row["Interest Rate"]),
                            monthly_installment=Decimal(row["Monthly payment"]),
                            emis_paid_on_time=int(row["EMIs paid on Time"]),
                            start_date=date_of_approval,
                            end_date=end_date,
                        )
                        loans_created += 1

                self.stdout.write(f"Created {loans_created} loans")

        except FileNotFoundError:
            raise CommandError(f"Loan file not found: {file_path}")
        except Exception as e:
            raise CommandError(f"Error importing loans: {str(e)}")
