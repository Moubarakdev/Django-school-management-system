# Generated by Django 4.1.1 on 2022-11-14 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_remove_user_employee_or_student_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomGroup',
        ),
    ]
