# Generated by Django 4.1.1 on 2022-09-24 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0012_remove_result_exams_subjectgroup_exams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectgroup',
            name='exams',
            field=models.ManyToManyField(blank=True, to='result.exam', verbose_name='examens'),
        ),
    ]