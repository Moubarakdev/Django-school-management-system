# Generated by Django 4.1.1 on 2022-11-16 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0020_remove_result_exam_remove_result_session_delete_exam'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subjectgroup',
            unique_together=set(),
        ),
    ]