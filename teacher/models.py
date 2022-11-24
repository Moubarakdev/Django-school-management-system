from django.core.validators import FileExtensionValidator
from django.db import models
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager

from academic.models import Department, AcademicSession, Subject
from myschool import settings

# Create your models here.
'''
class Designation(TimeStampedModel):
    title = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
'''


class Teacher(TimeStampedModel):
    last_name = models.CharField(max_length=150, verbose_name="nom")
    first_name = models.CharField(max_length=150, verbose_name="prénom")
    photo = models.ImageField(upload_to='teachers',
                              default='teacheravatar.jpg')
    date_of_birth = models.DateField(blank=True, null=True)
    expertise = TaggableManager(blank=True, verbose_name="Spécialisations")
    mobile_number = PhoneNumberField('Numéro de téléphone')
    email = models.CharField(max_length=255, blank=True, null=True)
    joining_date = models.DateField(auto_now=True)
    teacher_account = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="teacher_account",
        on_delete=models.DO_NOTHING, null=True)
    marksheet = models.FileField(
        upload_to='teachers/applicants/teacher_marksheets/%d/%m/%Y', verbose_name="Uploader votre dossier",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        help_text="Le fichier doit être scanner sous format pdf"
    )
    assigned_as_teacher = models.BooleanField(default=False, verbose_name="Assigné comme professeur")
    admission_date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['joining_date', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def name(self):
        return f'{self.last_name} {self.first_name} '


class TeacherSubjectGroup(TimeStampedModel):
    teacher = models.ForeignKey(
        "teacher.Teacher", on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name="Instructeur",
    )
    subjects = models.ManyToManyField(Subject, blank=True, verbose_name='matières')
    department = models.ForeignKey(
        Department,
        related_name='teacher_subjects',
        on_delete=models.DO_NOTHING, verbose_name='filière'
    )
    ac_session = models.ForeignKey(
        AcademicSession, on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name="Session académique"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)

    class Meta:
        unique_together = ['teacher', 'department', 'ac_session']
