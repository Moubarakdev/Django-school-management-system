# Generated by Django 4.1.1 on 2022-10-27 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0028_remove_admissionstudent_last_exam_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_inscription',
            field=models.BooleanField(default=False),
        ),
    ]