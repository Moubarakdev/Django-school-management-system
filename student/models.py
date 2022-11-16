import requests
from django.contrib import messages
from django.core.validators import FileExtensionValidator
from django.db import models, IntegrityError, transaction, OperationalError
from django.http import request
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from academic.models import Department, TempSerialID, AcademicSession
from myschool import settings
from payment.models import Invoice, InvoiceItem
from teacher.models import Teacher


# Create your models here.

class StudentBase(TimeStampedModel):
    GENDER = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
        ('N', 'Autre'),
    )
    RELIGION = (
        ('islam', 'islam'),
        ('christianisme', 'christianisme'),
        ('animisme', 'animisme'),
        ('athéisme', 'athéisme'),
        ('autre', 'autre'),
    )
    EXAM_NAMES = (
        ('L', 'Licence'),
        ('M', 'Master'),
        ('D', 'Doctorat'),
        ('', 'Aucun'),
    )
    last_name = models.CharField(verbose_name="Nom", max_length=100)
    first_name = models.CharField(verbose_name="Prénom", max_length=100)
    photo = models.ImageField(upload_to='students/applicant/')

    fathers_last_name = models.CharField(verbose_name="Nom du père", max_length=100)
    fathers_first_name = models.CharField(verbose_name="Prénom du père", max_length=100)
    fathers_mobile_number = PhoneNumberField(verbose_name="Numéro de téléphone du père", null=True, blank=True)

    mothers_last_name = models.CharField(verbose_name="Nom de la mère", max_length=100)
    mothers_first_name = models.CharField(verbose_name="Prénom de la mère", max_length=100)
    mothers_mobile_number = PhoneNumberField(verbose_name="Numéro de téléphone de la mère", null=True, blank=True)

    date_of_birth = models.DateField(verbose_name="Date de naissance")
    email = models.EmailField(verbose_name="Email")
    gender = models.CharField(verbose_name="Sexe", max_length=15, choices=GENDER)
    religion = models.CharField(verbose_name="Religion", max_length=30, choices=RELIGION)

    nationality = CountryField(blank=False,
                               null=True,
                               verbose_name="Nationalité")

    current_address = models.TextField(verbose_name='Adresse courante')
    permanent_address = models.TextField(verbose_name='Adresse permanente', blank=True, null=True)
    mobile_number = PhoneNumberField('Numéro de téléphone')
    guardian_mobile_number = PhoneNumberField('Numéro Personne à prévenir')

    department_choice = models.ForeignKey(
        Department,
        on_delete=models.CASCADE, verbose_name="Choix de la filière"
    )
    bac_passing_year = models.CharField(max_length=4, verbose_name="Année d'obtention du BAC")
    bac_marksheet = models.FileField(
        upload_to='students/applicants/bac_marksheets/%d/%m/%Y', verbose_name="Uploader votre relevé de BAC",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        help_text="Le fichier doit être scanner sous format pdf"
    )
    last_exam_marksheet = models.FileField(
        upload_to='students/applicants/last_marksheets/%d/%m/%Y', verbose_name="Autre document",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        help_text="Le fichier doit être scanner sous format pdf", blank=True, null=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.first_name


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_alumni=False,
            is_dropped=False
        )


class AlumniManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_alumni=True
        )


class CounselingComment(TimeStampedModel):
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, verbose_name="Conseiller"
    )
    registrant_student = models.ForeignKey(
        'AdmissionStudent',
        on_delete=models.CASCADE, null=True, verbose_name="Étudiant à inscrire"
    )
    comment = models.CharField(max_length=150, verbose_name="Commentaire du conseil")

    def __str__(self):
        date = self.created.strftime("%d %B %Y")
        return self.comment

    class Meta:
        ordering = ['-created', ]


class AdmissionStudent(StudentBase):
    APPLICATION_TYPE_CHOICE = (
        ('1', 'En ligne'),
        ('2', 'Hors ligne')
    )
    counseling_by = models.ForeignKey(
        Teacher, related_name='counselors',
        on_delete=models.CASCADE, null=True, verbose_name="Conseiller par"
    )
    counsel_comment = models.ManyToManyField(
        CounselingComment, blank=True, verbose_name="Commentaire du conseil"
    )
    choosen_department = models.ForeignKey(
        Department, related_name='admission_students',
        on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Filière courante"
    )
    admission_policy_agreement = models.BooleanField(
        """
        Accepter les conditions
        """,
        blank=False
    )
    admitted = models.BooleanField(default=False, verbose_name="Accepté")
    admission_date = models.DateField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="Payé")
    application_type = models.CharField(
        max_length=1,
        choices=APPLICATION_TYPE_CHOICE,
        default='1',
        verbose_name="Type d'application"
    )
    ac_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Session académique"
    )
    migration_status = models.CharField(
        max_length=255,
        blank=True, null=True
    )
    rejected = models.BooleanField(default=False, verbose_name="Rejeté")
    assigned_as_student = models.BooleanField(default=False, verbose_name="Assigné comme étudiant")
    student_account = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="student_account",
        on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.ac_session = AcademicSession.objects.get(current=True)
        self.fathers_last_name = self.fathers_last_name.upper()
        self.mothers_last_name = self.mothers_last_name.upper()
        self.fathers_first_name = self.fathers_first_name.capitalize()
        self.mothers_first_name = self.mothers_first_name.capitalize()
        self.mothers_last_name = self.mothers_last_name.upper()
        self.last_name = self.last_name.upper()
        self.first_name = self.first_name.capitalize()
        if self.department_choice != self.choosen_department:
            status = f'From {self.department_choice} to {self.choosen_department}'
            self.migration_status = status


class Student(TimeStampedModel):
    admission_student = models.ForeignKey(
        AdmissionStudent,
        on_delete=models.CASCADE, unique_for_year=True
    )
    temp_serial = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de série")
    temporary_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Id")
    ac_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Session académique"
    )
    admitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True
    )
    is_alumni = models.BooleanField(default=False, verbose_name="Ancien élève ?")
    is_dropped = models.BooleanField(default=False, verbose_name="A quitté l'école ?")
    assign_payment = models.BooleanField(default=False)

    # Managers
    objects = StudentManager()
    alumnus = AlumniManager()

    def __str__(self):
        return '{} ({}) {} filière.{}'.format(
            self.admission_student.last_name,
            self.admission_student.first_name,
            self.admission_student.choosen_department.level,
            self.admission_student.choosen_department,
        )

    def _find_last_admitted_student_serial(self):
        # What is the last temp_id for this year, dept?
        if not self.temp_serial or not self.temporary_id:
            item_serial_obj = TempSerialID.objects.filter(
                department=self.admission_student.choosen_department,
                year=self.admission_student.ac_session,
            ).order_by('serial').last()

            if item_serial_obj:
                # Return last temp_id
                serial_number = item_serial_obj.serial
                return int(serial_number)
            else:
                # If no temp_id object for this year and department found
                # return 0
                return 0

    def get_temp_id(self):
        if not self.temp_serial or not self.temporary_id:
            # Get current year (academic) last two digit
            year_digits = str(self.admission_student.ac_session.year)[-2:]
            # Get batch of student's department
            # batch_digits = self.batch.number
            # Get department code
            department_code = self.admission_student.choosen_department.code
            # Get admission serial of student by department
            temp_serial_key = self.temp_serial
            # return something like: 21-15-666-15
            temp_id = f'{year_digits}-' \
                      f'{department_code}-{temp_serial_key}'
            return temp_id

    def save(self, *args, **kwargs):
        if self.admission_student.ac_session:
            if self.admission_student.ac_session.year > self.ac_session.year:
                self.ac_session = self.admission_student.ac_session
            # Check if chosen_dept == batch.dept is same or not.
            if not self.admission_student.choosen_department.is_active:
                raise OperationalError(
                    f'Impossible d\'assigner la filière {self.admission_student.choosen_department} '
                    f'à l\'étudiant, vérifier si la filière est active')
            elif self.admission_student.choosen_department.is_active:
                # Set AdmissionStudent assigned_as_student=True
                self.admission_student.assigned_as_student = True
                self.admission_student.save()

        # Create temporary id for student id if temporary_id is not set yet.
        if not self.temp_serial or not self.temporary_id:
            last_temp_id = self._find_last_admitted_student_serial()
            current_temp_id = str(last_temp_id + 1)
            self.temp_serial = current_temp_id
            self.temporary_id = self.get_temp_id()
            super().save(*args, **kwargs)
            try:
                with transaction.atomic():
                    temp_serial_id = TempSerialID.objects.create(
                        student=self,
                        department=self.admission_student.choosen_department,
                        year=self.ac_session,
                        serial=current_temp_id
                    )
                    temp_serial_id.save()
            except IntegrityError:
                pass

        if not self.assign_payment:
            try:
                with transaction.atomic():
                    invoice = Invoice.objects.create(
                        student=self,
                        session=self.ac_session
                    )
                    invoiceItem = InvoiceItem.objects.create(
                        invoice=invoice,
                        description="Frais de scolarité",
                        amount=self.admission_student.choosen_department.fee
                    )
                    invoice.save()
                    invoiceItem.save()
                self.assign_payment = True

            except IntegrityError:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Override delete method """
        # If student is deleted, AdmissionStudent.assigned_as_student
        # should be false.
        self.admission_student.assigned_as_student = False
        self.admission_student.save(*args, **kwargs)


'''class RegularStudent(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Étudiant")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.student.admission_student.last_name} {self.student.admission_student.choosen_department.level}"'''
