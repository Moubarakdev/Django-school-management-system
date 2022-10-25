# Generated by Django 4.1.1 on 2022-10-20 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0023_remove_student_student_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionstudent',
            name='student_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_account', to=settings.AUTH_USER_MODEL),
        ),
    ]
