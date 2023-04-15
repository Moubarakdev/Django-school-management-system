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
        ('accounts', 'Comptabilité'),
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
        default='p',
    )
    requested_role = models.CharField(
        choices=REQUESTED_ACCOUNT_TYPE_CHOICES,
        max_length=50,
        default=REQUESTED_ACCOUNT_TYPE_CHOICES[0][0], verbose_name='Type de compte demandé'
    )
    approval_extra_note = models.TextField(
        blank=True, null=True, verbose_name='message'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.username = self.username.lower()
        self.first_name = self.first_name.capitalize()
        self.last_name = self.first_name.upper()


User._meta.get_field('email')._unique = True

'''
    def get_author_url(self):
       return reverse(
        'articles:author_profile',
        args=[self.username, ])

'''


'''class CustomGroup(Group):
    group_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name="créateur")

    def display_group(self):
        return f'{self.name} created by {self.group_creator}'

'''


class CommonUserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
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
    address = models.TextField(blank=True, null=True, verbose_name='Adresse')
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __str__(self):
        return f'{self.user}\'s profile'
