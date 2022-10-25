# Generated by Django 4.1.1 on 2022-10-07 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_alter_admissionstudent_religion_and_more'),
        ('payment', '0014_alter_studentfeesinfo_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentfeesinfo',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student', verbose_name='Étudiant'),
        ),
    ]