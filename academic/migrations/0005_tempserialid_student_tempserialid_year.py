# Generated by Django 4.1.1 on 2022-09-13 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('academic', '0004_tempserialid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempserialid',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_serial', to='student.student', verbose_name='Étudiant'),
        ),
        migrations.AddField(
            model_name='tempserialid',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.academicsession', verbose_name='Année académique'),
        ),
    ]
