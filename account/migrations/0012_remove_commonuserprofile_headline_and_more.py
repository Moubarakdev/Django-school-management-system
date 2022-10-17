# Generated by Django 4.1.1 on 2022-10-14 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_user_employee_or_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commonuserprofile',
            name='headline',
        ),
        migrations.RemoveField(
            model_name='commonuserprofile',
            name='show_headline_in_bio',
        ),
        migrations.RemoveField(
            model_name='commonuserprofile',
            name='social_links',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='commonuserprofile',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Adresse'),
        ),
        migrations.DeleteModel(
            name='SocialLink',
        ),
    ]
