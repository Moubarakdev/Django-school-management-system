from django.db import models, OperationalError
from django.urls import reverse
from model_utils.models import TimeStampedModel

from myschool import settings
from teacher.models import Teacher


# Create your models here.
# Department #filiere #serie
class Department(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Nom de département')
    code = models.PositiveIntegerField(verbose_name="Code department ")
    description = models.TextField(help_text='Ecriver une simple description a propos du département', blank=True,
                                   null=True, verbose_name='Description')
    current_batch = models.ForeignKey('Batch', on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='current_batches',
                                      verbose_name='Promotion actuelle')
    batches = models.ManyToManyField('Batch', related_name='department_batches', blank=True, verbose_name="Promotions")
    establish_date = models.DateField(auto_now_add=True, verbose_name='Date de création')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                   null=True, verbose_name="Créateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return str(self.name)


class AcademicSession(TimeStampedModel):
    year = models.PositiveIntegerField(unique=True, verbose_name="Année")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True, verbose_name="Créateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return '{} - {}'.format(self.year, self.year + 1)

    @property
    def academic_year(self):
        return '{} - {}'.format(self.year, self.year + 1)


def create_resource():
    return reverse('dashboard:academic:create_semester')


class Semester(TimeStampedModel):
    number = models.PositiveIntegerField(unique=True, verbose_name='Numéro semestre')
    '''
      guide = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        default=None, null=True, blank=True
      )
    '''
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    class Meta:
        ordering = ['number', ]

    def __str__(self):
        if self.number == 1:
            return 'Semestre 1'
        if self.number == 2:
            return 'Semestre 2'
        if self.number == 3:
            return 'Semestre 3'
        if self.number and 3 < self.number <= 12:
            return 'Semestre ' + '%s' % self.number

    @property
    def active_or_not(self):
        return "Oui" if self.active else "Non"


class Subject(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="Titre du cours")
    subject_code = models.CharField(unique=True, verbose_name="Code cours", max_length=50)
    instructor = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Instructeur"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return "{} ({})".format(self.name, self.subject_code)


class Batch(TimeStampedModel):
    year = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name="Année scolaire")
    number = models.PositiveIntegerField('Numéro promotion')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Département')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    class Meta:
        verbose_name_plural = 'Promotions'
        unique_together = ['year', 'department', 'number']

    def __str__(self):
        return f'{self.department.name} Batch {self.number} ({self.year})'


class TempSerialID(TimeStampedModel):
    student = models.OneToOneField('student.Student', on_delete=models.CASCADE,
                                   related_name='student_serial', verbose_name="Étudiant")
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='temp_serials', verbose_name="Département")
    year = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name="Année académique")
    serial = models.CharField(max_length=50, blank=True, verbose_name="Numéro de série")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    # class Meta:
    #     unique_together = ['department', 'year']

    def __str__(self):
        return self.serial

    def save(self, *args, **kwargs):
        if self.student.admission_student.admitted:
            super().save(*args, **kwargs)
        else:
            raise OperationalError('Please check if student is admitted or not.')

    def get_serial(self):
        # Get current year last two digit
        yf = str(self.student.ac_session)[-2:]
        # Get current batch of student's department
        bn = self.student.batch.number
        # Get department code
        dc = self.department.code
        # Get admission serial of student by department
        syl = self.serial

        # return something like: 21-15-666-15
        return f'{yf}-{bn}-{dc}-{syl}'


