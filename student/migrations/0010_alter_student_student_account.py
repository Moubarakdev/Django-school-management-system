# Generated by Django 4.1.1 on 2022-10-05 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0009_alter_admissionstudent_admission_policy_agreement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]