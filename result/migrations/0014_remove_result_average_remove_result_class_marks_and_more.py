# Generated by Django 4.1.1 on 2022-09-24 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_alter_admissionstudent_counsel_comment_and_more'),
        ('academic', '0012_remove_subject_class_marks_remove_subject_exam_marks_and_more'),
        ('result', '0013_alter_subjectgroup_exams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='average',
        ),
        migrations.RemoveField(
            model_name='result',
            name='class_marks',
        ),
        migrations.RemoveField(
            model_name='result',
            name='exam_marks',
        ),
        migrations.RemoveField(
            model_name='result',
            name='extra_marks',
        ),
        migrations.RemoveField(
            model_name='result',
            name='validated',
        ),
        migrations.RemoveField(
            model_name='subjectgroup',
            name='exams',
        ),
        migrations.AddField(
            model_name='result',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='result.exam', verbose_name='Examen'),
        ),
        migrations.AddField(
            model_name='result',
            name='practical_marks',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Note de classe'),
        ),
        migrations.AddField(
            model_name='result',
            name='theory_marks',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="Note d'examen"),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_name',
            field=models.CharField(choices=[('d', 'Devoir'), ('e', 'Examen'), ('r', 'Rattrapage')], max_length=1, verbose_name="titre de l'examen"),
        ),
        migrations.AlterField(
            model_name='result',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.semester'),
        ),
        migrations.AlterField(
            model_name='result',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='student.student'),
        ),
        migrations.AlterField(
            model_name='result',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.subject'),
        ),
        migrations.AlterField(
            model_name='result',
            name='total_marks',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Total'),
        ),
    ]
