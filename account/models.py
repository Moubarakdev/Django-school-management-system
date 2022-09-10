from django.contrib.auth.models import AbstractUser
from django.shortcuts import render
from django.db import models
from django_countries.fields import CountryField


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


class CommonUserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Utilisateur"
    )
    profile_picture = models.ImageField(
        upload_to='profile-pictures',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    cover_picture = models.ImageField(
        upload_to='cover-pictures',
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
        help_text='I want to use this as my bio',
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
