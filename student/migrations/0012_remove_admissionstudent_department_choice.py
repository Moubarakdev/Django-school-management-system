# Generated by Django 4.1.1 on 2022-10-05 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_alter_student_student_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admissionstudent',
            name='department_choice',
        ),
    ]
