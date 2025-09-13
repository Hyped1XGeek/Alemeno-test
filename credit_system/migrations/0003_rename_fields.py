# Generated manually to rename fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credit_system', '0002_auto_20250912_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='monthly_salary',
            new_name='monthly_income',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='monthly_payment',
            new_name='monthly_installment',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='date_of_approval',
            new_name='start_date',
        ),
    ]
