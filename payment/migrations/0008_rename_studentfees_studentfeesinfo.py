# Generated by Django 4.1.1 on 2022-10-05 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_alter_student_student_account'),
        ('payment', '0007_studentfees_payment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentFees',
            new_name='StudentFeesInfo',
        ),
    ]