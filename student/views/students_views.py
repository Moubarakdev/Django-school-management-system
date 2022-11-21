import os
from collections import OrderedDict
from datetime import datetime, timedelta, date

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import FileSystemStorage, DefaultStorage
from django.db import IntegrityError
from django.forms.models import construct_instance
from django.http import JsonResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView
from formtools.wizard.views import SessionWizardView
from rolepermissions.roles import assign_role

from academic.models import AcademicSession, Department
from account.models import User
from myschool import settings
from payment.models import Invoice
from permission_handlers.administrative import user_is_admin_su_or_ac_officer
from permission_handlers.basic import user_is_verified, user_is_student
from result.models import SubjectGroup
from student.filters import AlumniFilter
from student.forms import AdmissionForm, StudentRegistrantUpdateForm, CounselingDataForm, StudentForm, \
    StudentUpdateForm, AdmissionForm2
from student.models import AdmissionStudent, Student, CounselingComment


@user_passes_test(user_is_admin_su_or_ac_officer)
def students_board(request):
    """
    Dashboard for online admission system.
    """
    unpaid_registrants = AdmissionStudent.objects.filter(paid=False)
    all_applicants = AdmissionStudent.objects.all().order_by('-created')
    admitted_students = AdmissionStudent.objects.filter(admitted=True, assigned_as_student=False)
    paid_registrants = AdmissionStudent.objects.filter(paid=True, admitted=False, assigned_as_student=False)
    rejected_applicants = AdmissionStudent.objects.filter(rejected=True)
    offline_applicants = AdmissionStudent.objects.filter(application_type='2')
    waiting_for_confirmation = AdmissionStudent.objects.filter(paid=True, admitted=True, assigned_as_student=False)

    # List of months since first application registration date
    try:
        first_application_date = AdmissionStudent.objects.order_by(
            'created')[0].created.date()
        last_application_date = date.today()
        dates = [str(first_application_date), str(last_application_date)]
        months_start, months_end = [
            datetime.strptime(_, '%Y-%m-%d') for _ in dates
        ]
        # List of month to display options in student dashboard index
        month_list = OrderedDict(
            ((months_start + timedelta(_)).strftime(r"%B-%Y"), None) for _ in
            range((months_end - months_start).days)
        ).keys()
    except IndexError:
        month_list = []

    context = {
        'all_applicants': all_applicants,
        'unpaid_registrants': unpaid_registrants,
        'admitted_students': admitted_students,
        'paid_registrants': paid_registrants,
        'rejected_applicants': rejected_applicants,
        'offline_applicants': offline_applicants,
        'month_list': month_list,
        'waiting_for_confirmation': waiting_for_confirmation
    }
    return render(request, 'students/students_board.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def all_applicants(request):
    """Display all registered students list"""
    registrants = AdmissionStudent.objects.all().order_by('-created')
    ctx = {
        'registrants': registrants,
    }
    return render(request, 'students/all_applicants.html', ctx)


@user_passes_test(user_is_admin_su_or_ac_officer)
def admitted_students_list(request):
    """
    Returns list of students admitted from online registration.
    """
    admitted_students = AdmissionStudent.objects.filter(admitted=True, assigned_as_student=False)
    context = {
        'admitted_students': admitted_students,
    }
    return render(request, 'students/dashboard_all_cleared_students.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def paid_registrants(request):
    """
    Returns list of students already paid from online registration.
    """
    paid_students = AdmissionStudent.objects.filter(paid=True, admitted=True, assigned_as_student=False)
    context = {
        'paid_students': paid_students,
    }
    return render(request, 'students/dashboard_paid_students.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def unpaid_registrants(request):
    """
    Returns list of students haven't paid admission fee yet.
    """
    unpaid_registrants_list = AdmissionStudent.objects.filter(paid=False)
    context = {
        'unpaid_applicants': unpaid_registrants_list,
    }
    return render(request, 'students/unpaid_applicants.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def rejected_registrants(request):
    ctx = {
        'rejected_registrants': AdmissionStudent.objects.filter(rejected=True),
    }
    return render(request, 'students/list/rejected_registrants.html', ctx)


'''
def get_json_batch_data(request, *args, **kwargs):
    selected_department_code = kwargs.get('department_code')
    department_batches = list(
        Batch.objects.filter(department__code=selected_department_code).values()
    )
    return JsonResponse({'data': department_batches})
'''


@user_passes_test(user_is_admin_su_or_ac_officer)
def admission_confirmation(request):
    """
    If request is get, show list of applicants to be admitted finally as student,
    for POST request, it will create Student, RegularStudent.
    """
    selected_registrants = AdmissionStudent.objects.filter(
        admitted=True,
        paid=True,
        rejected=False,
        assigned_as_student=False)
    departments = Department.objects.filter(is_active=True).order_by('name')
    sessions = AcademicSession.objects.filter(current=True)
    ctx = {
        'selected_registrants': selected_registrants,
        'departments': departments,
        'sessions': sessions,
    }

    if request.method == 'POST':
        dept_code = request.POST.get('department_code')
        session_id = request.POST.get('session_id')
        # If confirmation processes is followed by checkmarks,
        # then we confirm admission for only selected candidates.
        checked_registrant_ids = request.POST.getlist('registrant_choice')
        try:
            to_be_admitted = selected_registrants.filter(
                choosen_department__code=int(dept_code)
            )
            if checked_registrant_ids:
                to_be_admitted = AdmissionStudent.objects.filter(
                    id__in=list(map(int, checked_registrant_ids))
                )
        except ValueError:
            messages.add_message(
                request,
                messages.ERROR,
                'Veuillez sélectionner les candidats à autoriser pour l`\'admission.'
            )
            to_be_admitted = []

        students = []
        for candidate in to_be_admitted:
            try:
                session = AcademicSession.objects.get(id=session_id)
            except ValueError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Veuillez choisir une session valide.'
                )
            # If student.save() doesn't raise any exceptions,
            # we save student, except, we skip making student object.
            try:
                student = Student.objects.create(
                    admission_student=candidate,
                    ac_session=session,
                    admitted_by=request.user,
                )
                students.append(student)
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Inscription confirmée avec succès'
                )
            except:
                pass

        ctx['students'] = students
        return render(request, 'students/list/confirm_admission.html', ctx)
    else:
        return render(request, 'students/list/confirm_admission.html', ctx)


@user_passes_test(user_is_admin_su_or_ac_officer)
def admit_student(request, pk):
    """
    Admit applicant found by id/pk into chosen department
    """
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=applicant)
        if form.is_valid():
            student = form.save(commit=False)
            student.admitted = True
            # student.paid = True
            student.admission_date = date.today()
            student.save()
            # prévoir l'envoi de l'email de confirmation
            # send_admission_confirmation_email.delay(student.id)
            messages.add_message(request, messages.SUCCESS, "Demande validée avec succès")
            return redirect('dashboard:student:admitted_student_list')
    else:
        form = AdmissionForm()
        context = {'form': form, 'applicant': applicant}
    return render(request, 'students/dashboard_admit_student.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def reject_student(request, pk):
    """
    reject applicant found by id/pk into chosen department
    """
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=applicant)
        if form.is_valid():
            student = form.save(commit=False)
            student.rejected = True
            student.save()
            # prévoir l'envoi de l'email de confirmation
            # send_admission_confirmation_email.delay(student.id)
            return redirect('dashboard:student:rejected_registrant_list')
    else:
        form = AdmissionForm()
        context = {'form': form, 'applicant': applicant}
    return render(request, 'students/list/rejected_registrants.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def renew_admission(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm2(request.POST, files=request.FILES, instance=student.admission_student)
        if form.is_valid():
            new = AdmissionStudent.objects.create(**form.cleaned_data)
            student.admission_student = new
            student.assign_payment = False
            student.save()
            return redirect('dashboard:student:student_details', pk=pk)
        else:
            print(form.errors)
            messages.add_message(
                request,
                messages.ERROR,
                'Problem',
            )
    else:
        form = AdmissionForm2(instance=student.admission_student)
    context = {'form': form, 'student': student}
    return render(request, 'students/new_admission.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def mark_as_paid_or_unpaid(request):
    """ Change student applicants payment status """
    if request.method == 'POST':
        registrant_pk = request.POST.get('registrant_id')
        applicant = get_object_or_404(AdmissionStudent, pk=registrant_pk)
        if not applicant.paid:
            # If applicant didn't pay fee already, change to paid
            applicant.paid = True
            applicant.save()
            return JsonResponse({'data': True})
        # If applicant already paid the amount, change to unpaid
        applicant.paid = False
        applicant.save()
        return JsonResponse({'data': False})


@user_passes_test(user_is_admin_su_or_ac_officer)
def update_online_registrant(request, pk):
    """
    Update applicants details, counseling information
    """
    applicant = get_object_or_404(AdmissionStudent, pk=pk)
    counseling_records = CounselingComment.objects.filter(registrant_student=applicant)
    if request.method == 'POST':
        form = StudentRegistrantUpdateForm(
            request.POST,
            request.FILES,
            instance=applicant)
        if form.is_valid():
            form.save()
            # return redirect('dashboard:student:paid_registrant_list')
            messages.add_message(request, messages.SUCCESS, "Demande modifiée avec succès")
            return redirect('dashboard:student:registration_details', pk=pk)
    else:
        form = StudentRegistrantUpdateForm(instance=applicant)
        counseling_form = CounselingDataForm()
        context = {
            'form': form,
            'applicant': applicant,
            'counseling_records': counseling_records,
            'counseling_form': counseling_form}
    return render(request, 'students/dashboard_update_online_applicant.html', context)


class RegistrationDetails(DetailView):
    model = AdmissionStudent
    template_name = 'students/registration_details.html'
    context_object_name = 'applicant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        applicant_id = self.kwargs['pk']
        applicant = get_object_or_404(AdmissionStudent, pk=applicant_id)
        context['counseling_records'] = CounselingComment.objects.filter(registrant_student=applicant)
        context['counseling_form'] = CounselingDataForm()
        return context


@user_passes_test(user_is_admin_su_or_ac_officer)
def add_counseling_data(request, student_id):
    registrant = get_object_or_404(AdmissionStudent, id=student_id)
    if request.method == 'POST':
        form = CounselingDataForm(request.POST)
        if form.is_valid():
            counseling_comment = form.save(commit=False)
            counseling_comment.counselor = request.user
            counseling_comment.registrant_student = registrant
            counseling_comment.save()
            return redirect('dashboard:student:registration_details', pk=student_id)


@user_passes_test(user_is_admin_su_or_ac_officer)
def add_student_view(request):
    """
    :param request:
    :return: admission form to
    logged in user.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            # check student as offline registration
            student.application_type = '2'
            student.save()
            return redirect('dashboard:student:all_applicants')
    else:
        form = StudentForm()
    context = {'form': form}
    return render(request, 'students/addstudent.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def students_view(request):
    """
    :param request:
    :return: renders student list with all department
    and semesters list.
    """
    all_students = Student.objects.select_related(
        'admission_student', 'ac_session').all()
    context = {
        'students': all_students,
    }
    return render(request, 'students/list/students_list.html', context)


@user_passes_test(user_is_admin_su_or_ac_officer)
def students_by_department_view(request, pk):
    dept_name = Department.objects.get(pk=pk)
    students = Student.objects.select_related(
        'department', 'ac_session').filter(department=dept_name)
    context = {'students': students, }
    return render(request, 'students/students_by_department.html', context)


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    renders a student update form to update students details.
    """
    model = Student
    form_class = StudentUpdateForm
    template_name = 'students/update_student.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')

    def post(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Student, pk=pk)
        form = StudentUpdateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:student:student_details', pk=obj.pk)

    def get_success_url(self):
        student_id = self.kwargs['pk']
        return reverse_lazy('dashboard:student:student_details', kwargs={'pk': student_id})


class StudentDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'students/student_details.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = kwargs['object']
        pk = obj.id
        student = Student.objects.get(pk=pk)
        # get student object
        # for showing subjects in option form
        student_subject_qs = SubjectGroup.objects.filter(
            department=student.admission_student.choosen_department,
        )
        context['subjects'] = student_subject_qs
        # getting result objects
        results = student.results.all()
        context['results'] = results
        context["payments"] = Invoice.objects.filter(student=self.object).order_by('-session')
        return context


@user_passes_test(user_is_admin_su_or_ac_officer)
def student_delete_view(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('dashboard:student:all_student')


class AlumnusListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Student
    context_object_name = 'alumnus'
    template_name = 'students/list/alumnus.html'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')

    def get_queryset(self):
        queryset = Student.alumnus.all()
        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        ctx = super().get_context_data(*args, object_list=object_list, **kwargs)
        alumnus = Student.alumnus.all()
        f = AlumniFilter(self.request.GET, queryset=alumnus)
        ctx['filter'] = f
        return ctx


# APPLICATION
class ApplicationWizard(LoginRequiredMixin, SessionWizardView):
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form)
        # check if the student have an account
        try:
            student = AdmissionStudent.objects.get(student_account=self.request.user)
        except:
            student = None
        if student:
            # check if the student is admitted and confirmed
            if student.assigned_as_student:
                ac_st = self.request.user
                # approuve the account of the student an assign him his role
                ac_st.approval_status = 'a'
                assign_role(ac_st, 'student')
                ac_st.save()

        print(student)
        context['student'] = student
        return context

    template_name = 'students/applications/application_form.html'
    file_storage = DefaultStorage()

    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        if self.request.user.is_authenticated:
            form_data['student_account'] = self.request.user
        try:
            AdmissionStudent.objects.create(**form_data)
        except IntegrityError:
            pass

        return render(self.request, 'students/applications/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


@user_passes_test(user_is_student)
def studentSubjectView(request):
    student = Student.objects.get(admission_student__student_account=request.user)
    # get student object
    # for showing subjects in option form
    student_subject_qs = SubjectGroup.objects.filter(
        department=student.admission_student.choosen_department,
    )
    subjects = student_subject_qs
    context = {
        'student': student,
        'subjects': subjects,
    }
    return render(request, 'students/connect/student_subjects.html', context)


@user_passes_test(user_is_student)
def studentResultView(request):
    student = Student.objects.get(admission_student__student_account=request.user)
    # get student object
    # getting result objects
    results = student.results.all()
    context = {
        'student': student,
        'results': results
    }
    return render(request, 'students/connect/student_results.html', context)
