"""
Credit System Django App Configuration.
"""

from django.apps import AppConfig


class CreditSystemConfig(AppConfig):
    """Configuration for the Credit System app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "credit_system"
    verbose_name = "Credit Approval System"
