# Generated by Django 4.1.1 on 2022-10-25 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0022_invoice_balance_from_previous_term'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='balance_from_previous_term',
            new_name='balance_from_previous_session',
        ),
    ]
