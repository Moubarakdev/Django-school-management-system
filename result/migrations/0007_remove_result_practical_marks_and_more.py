# Generated by Django 4.1.1 on 2022-09-23 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0006_remove_result_average_remove_result_exam_marks_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='practical_marks',
        ),
        migrations.RemoveField(
            model_name='result',
            name='theory_marks',
        ),
        migrations.AddField(
            model_name='result',
            name='average',
            field=models.FloatField(blank=True, null=True, verbose_name='moyenne'),
        ),
        migrations.AddField(
            model_name='result',
            name='exam_marks',
            field=models.FloatField(blank=True, null=True, verbose_name="note d'examen"),
        ),
        migrations.AddField(
            model_name='result',
            name='extra_marks',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='note de rattrapage'),
        ),
        migrations.AddField(
            model_name='result',
            name='validated',
            field=models.BooleanField(blank=True, default='False', verbose_name='Validé ?'),
        ),
        migrations.AlterField(
            model_name='result',
            name='total_marks',
            field=models.FloatField(blank=True, null=True, verbose_name='total notes'),
        ),
    ]
