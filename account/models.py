from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser, Group
from django.shortcuts import render
from django.db import models
from django_countries.fields import CountryField

from myschool import settings


# Create your models here.

class User(AbstractUser):
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ('subscriber', 'Abonné'),
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
        ('editor', 'Editeur'),
        ('academic_officer', 'Direction Académique'),
        ('admin', 'Administrateur'),
    )
    APPROVAL_CHOICES = (
        ('n', 'Aucune demande d\'approbation'),
        ('p', 'Demande d’approbation en attente'),
        ('d', 'Demande d’approbation refusée'),
        ('a', 'Vérifié')
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_CHOICES,
        default='n',
    )
    employee_or_student_id = models.CharField(
        help_text="seulement si vous êtes déjà Étudiant ou Professeur",
        max_length=10,
        blank=True, null=True, verbose_name='Matricule'
    )
    requested_role = models.CharField(
        choices=REQUESTED_ACCOUNT_TYPE_CHOICES,
        max_length=50,
        default=REQUESTED_ACCOUNT_TYPE_CHOICES[0][0], verbose_name='Type de compte'
    )
    approval_extra_note = models.TextField(
        blank=True, null=True, verbose_name='message'
    )
    address = models.TextField(blank=True, null=True, verbose_name='Adresse')


User._meta.get_field('email')._unique = True

'''
    def get_author_url(self):
       return reverse(
        'articles:author_profile',
        args=[self.username, ])

'''


class CustomGroup(Group):
    group_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name="créateur")

    def display_group(self):
        return f'{self.name} created by {self.group_creator}'


class SocialLink(models.Model):
    user_profile = models.ForeignKey(
        'CommonUserProfile',
        on_delete=models.CASCADE
    )
    media_name = models.CharField(
        max_length=50, verbose_name='Nom'
    )
    url = models.URLField()

    def __str__(self):
        return self.media_name


class CommonUserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Utilisateur"
    )
    profile_picture = models.ImageField(
        upload_to='users/profile-pictures',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    cover_picture = models.ImageField(
        upload_to='users/cover-pictures',
        blank=True,
        null=True,
        verbose_name="Photo de couverture"
    )
    headline = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Titre"
    )

    show_headline_in_bio = models.BooleanField(
        help_text='je veux utilisé ceci comme ma bio',
        default=False,
        verbose_name="Titre comme bio"
    )
    summary = RichTextUploadingField(
        help_text='un petit résumé de votre profil',
        blank=True,
        null=True,
        verbose_name='Résumé du profil'
    )
    country = CountryField(
        blank=True,
        null=True,
        verbose_name="Pays"
    )
    social_links = models.ManyToManyField(
        SocialLink,
        related_name='social_links',
        blank=True, verbose_name='Réseau social'
    )

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __str__(self):
        return f'{self.user}\'s profile'
