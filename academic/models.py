from django.db import models, OperationalError
from django.urls import reverse
from model_utils.models import TimeStampedModel

from myschool import settings
from teacher.models import Teacher


# Create your models here.
# Department #filiere #serie

class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class Department(TimeStampedModel):
    LEVEL_CHOICES = (
        ('lp1', 'LP1'),
        ('lp2', 'LP2'),
        ('lp3', 'LP3'),
        ('m1', 'M1'),
        ('m2', 'M2'),
    )
    name = models.CharField(max_length=255, verbose_name='Nom de la filière')
    code = models.PositiveIntegerField(verbose_name="Code filière ")
    description = models.TextField(help_text='Ecriver une simple description a propos de la filière', blank=True,
                                   null=True, verbose_name='Description')
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='LP1', verbose_name="Niveau")
    establish_date = models.DateField(auto_now_add=True, verbose_name='Date de création')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                   null=True, verbose_name="Créateur")
    fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Frais de scolarité")
    is_active = models.BooleanField(verbose_name="Actif", default="True")

    class Meta:
        verbose_name_plural = 'Filières'
        unique_together = ['name', 'code', 'level']

    def __str__(self):
        return f"{str(self.name)} - {str(self.level).upper()}"

    def save(self, *args, **kwargs):
        last_dept = Department.objects.last()
        self.code = last_dept.code + 1
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class AcademicSession(TimeStampedModel):
    year = models.PositiveIntegerField(unique=True, verbose_name="Année académique")
    current = models.BooleanField(default=True, verbose_name="Marquer comme année courante")
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


'''class AcademicTerm(models.Model):
    """Academic Term"""

    name = models.CharField(max_length=20, unique=True, verbose_name="Nom")
    current = models.BooleanField(default=True, verbose_name="Période courante")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

'''
"""
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

"""


class Subject(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="Titre du cours")
    subject_code = models.CharField(unique=True, verbose_name="Code cours", max_length=50)
    instructor = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Instructeur"
    )
    hourly_volume = models.IntegerField(blank=True, default=0,
                                        null=True, verbose_name="Volume horaire")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return "{} ({})".format(self.name, self.subject_code)


"""
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

"""


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
        # bn = self.student.batch.number
        # Get department code
        dc = self.department.code
        # Get admission serial of student by department
        syl = self.serial

        # return something like: 21-15-666-15
        # return f'{yf}-{bn}-{dc}-{syl}'
        return f'{yf}-{dc}-{syl}'


'''
class GroupFees(TimeStampedModel):
    """ Keep track of group of subjects that belongs to a
        department, semesters
        """
    department = models.ForeignKey(
        Department,
        related_name='subjects',
        on_delete=models.DO_NOTHING, verbose_name='département'
    )
    semesters = models.ManyToManyField(
        Semester,
        verbose_name='semestres',
        limit_choices_to=2, blank=True
    )
    description = models.CharField(verbose_name="Description", max_length=15)
    fees_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant des frais")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")
'''
