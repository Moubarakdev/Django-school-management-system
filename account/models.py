from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser, Group
from django.shortcuts import render
from django.db import models
from django_countries.fields import CountryField

from myschool import settings


# Create your views here.

class User(AbstractUser):
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ('subscriber', 'Subscriber'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('editor', 'Editor'),
        ('academic_officer', 'Academic Officer'),
        ('admin', 'Admin'),
    )
    APPROVAL_CHOICES = (
        ('n', 'Not Requested For Approval'),
        ('p', 'Approval Application on Pending'),
        ('d', 'Approval Request Declined'),
        ('a', 'Verified')
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_CHOICES,
        default='n',
    )
    employee_or_student_id = models.CharField(
        max_length=10,
        blank=True, null=True
    )
    requested_role = models.CharField(
        choices=REQUESTED_ACCOUNT_TYPE_CHOICES,
        max_length=50,
        default=REQUESTED_ACCOUNT_TYPE_CHOICES[0][0]
    )
    approval_extra_note = models.TextField(
        blank=True, null=True
    )


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
        max_length=50, verbose_name='Nom du média'
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
        help_text='Je veux utiliser ceci comme ma bio',
        default=False,
        verbose_name="Titre comme bio"
    )
    summary = RichTextUploadingField(
        help_text='Your Profile Summary',
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
        blank=True
    )

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user}\'s profile'
