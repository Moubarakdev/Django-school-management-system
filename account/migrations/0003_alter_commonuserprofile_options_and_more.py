# Generated by Django 4.1.1 on 2022-09-13 19:42

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_commonuserprofile_cover_picture_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commonuserprofile',
            options={'verbose_name': 'Profil', 'verbose_name_plural': 'Profils'},
        ),
        migrations.AlterField(
            model_name='commonuserprofile',
            name='show_headline_in_bio',
            field=models.BooleanField(default=False, help_text='je veux utilisé ceci comme ma bio', verbose_name='Titre comme bio'),
        ),
        migrations.AlterField(
            model_name='commonuserprofile',
            name='social_links',
            field=models.ManyToManyField(blank=True, related_name='social_links', to='account.sociallink', verbose_name='Réseau social'),
        ),
        migrations.AlterField(
            model_name='commonuserprofile',
            name='summary',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='un petit résumé de votre profil', null=True, verbose_name='Résumé du profil'),
        ),
        migrations.AlterField(
            model_name='sociallink',
            name='media_name',
            field=models.CharField(max_length=50, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='approval_extra_note',
            field=models.TextField(blank=True, null=True, verbose_name='message'),
        ),
        migrations.AlterField(
            model_name='user',
            name='approval_status',
            field=models.CharField(choices=[('n', "Aucune demande d'approbation"), ('p', 'Demande d’approbation en attente'), ('d', 'Demande d’approbation refusée'), ('a', 'Vérifié')], default='n', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='employee_or_student_id',
            field=models.CharField(blank=True, help_text='seulement si vous êtes déjà Étudiant ou Professeur', max_length=10, null=True, verbose_name='Matricule'),
        ),
        migrations.AlterField(
            model_name='user',
            name='requested_role',
            field=models.CharField(choices=[('subscriber', 'Abonné'), ('student', 'Étudiant'), ('teacher', 'Professeur'), ('editor', 'Editeur'), ('academic_officer', 'Direction Académique'), ('admin', 'Administrateur')], default='subscriber', max_length=50, verbose_name='Type de compte'),
        ),
    ]
