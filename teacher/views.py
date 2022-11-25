from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from rolepermissions.roles import assign_role

from academic.models import Department, Subject
from permission_handlers.administrative import user_is_admin_su_or_ac_officer, user_is_teacher_or_administrative
from permission_handlers.basic import user_is_verified
from result.filters import SubjectGroupFilter, TeacherSubjectGroupFilter
from result.forms import CreateResults, EditResults
from result.models import SubjectGroup, Result
from student.models import Student
from teacher.forms import TeacherForm, TeacherSubjectsForm
from teacher.models import Teacher, TeacherSubjectGroup


# Create your views here.
class CreateTeacherView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Teacher
    form_class = TeacherForm

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:teacher:read_teachers')
    template_name = 'teacher/teacher_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateTeacherView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teacher/teacher_form.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:teacher:read_teachers')


class TeacherListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Teacher
    queryset = Teacher.objects.filter(assigned_as_teacher=True)
    context_object_name = "teachers"
    template_name = 'teacher/teacher_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')


class DeleteTeacherView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Teacher
    template_name = 'teacher/teacher_confirm_delete.html'
    success_url = reverse_lazy('dashboard:teacher:read_teachers')

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')


class TeacherDetailView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Teacher
    template_name = 'teacher/teacher_detail.html'
    context_object_name = 'teacher'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('profile_complete')
        return redirect('login')


class TeacherApplication(CreateView, LoginRequiredMixin):
    model = Teacher
    form_class = TeacherForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # check if the student have an account
        try:
            teacher = Teacher.objects.get(teacher_account=self.request.user)
        except:
            teacher = None

        if teacher:
            # check if the student is admitted and confirmed
            if teacher.assigned_as_teacher:
                ac_th = self.request.user
                # approuve the account of the student an assign him his role
                ac_th.approval_status = 'a'
                assign_role(ac_th, 'teacher')
                ac_th.save()

        context['teacher'] = teacher
        return context

    success_url = reverse_lazy('dashboard:teacher:teacher_application')
    template_name = 'applications/application_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.teacher_account = self.request.user
        return super().form_valid(form)


@user_passes_test(user_is_admin_su_or_ac_officer)
def all_applicants(request):
    """Display all registered students list"""
    registrants = Teacher.objects.filter(assigned_as_teacher=False).order_by('-created')
    ctx = {
        'registrants': registrants,
    }
    return render(request, 'teacher/list/all_applicants.html', ctx)


@user_passes_test(user_is_admin_su_or_ac_officer)
def admit_teacher(request, pk):
    """
    Admit applicant found by id/pk into chosen department
    """
    applicant = get_object_or_404(Teacher, pk=pk)
    applicant.assigned_as_teacher = True
    applicant.admission_date = date.today()
    applicant.save()
    # prévoir l'envoi de l'email de confirmation
    # send_admission_confirmation_email.delay(student.id)
    return redirect('dashboard:teacher:read_teachers')


@user_passes_test(user_is_teacher_or_administrative)
def create_teacher_subject_group(request):
    ctx = {}
    if not request.GET:
        qs = SubjectGroup.objects.none()
    else:
        qs = SubjectGroup.objects.all()

    subject_group_filter = SubjectGroupFilter(
        request.GET,
        queryset=qs
    )

    department = None
    for subject_group in subject_group_filter.qs:
        department = Department.objects.get(pk=subject_group.department.pk)
    ctx.update({
        'department': department,
    })

    teachers = Teacher.objects.all()

    if request.method == 'POST':
        dept_pk = int(request.POST.get('department'))
        subject_list = request.POST.getlist('subject')
        teacher_pk = int(request.POST.get('teacher'))

        dept = Department.objects.get(pk=dept_pk)
        teacher = Teacher.objects.get(pk=teacher_pk)
        try:
            teacher_subject_group = TeacherSubjectGroup.objects.create(
                teacher=teacher,
                department=dept,
                ac_session=request.current_session
            )
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                 "Des cours ont déjà été assignés à ce professeur, pour en ajouter veuillez "
                                 "plutôt choisir l'option modifier")
            return redirect('dashboard:teacher:teacher_subject_groups')

        subject_objects = []
        for s_pk in subject_list:
            subj = Subject.objects.get(pk=int(s_pk))
            subject_objects.append(subj)
            teacher_subject_group.subjects.add(subj)

        teacher_subject_group.save()
        return redirect('dashboard:teacher:teacher_subject_groups')
    ctx.update({
        'subject_group_filter': subject_group_filter,
        'department': department,
        'teachers': teachers
    })
    return render(request, 'teacher/create_teacher_subjects_group.html', ctx)


@user_passes_test(user_is_verified)
def teacher_subject_group_list(request):
    subject_groups = TeacherSubjectGroup.objects.all()
    ctx = {
        'subject_groups': subject_groups,
    }
    return render(request, 'teacher/teacher_subject_group_list.html', ctx)


class UpdateTeacherSubjectGroup(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TeacherSubjectGroup
    form_class = TeacherSubjectsForm
    template_name = 'teacher/teacher_subject_group_form.html'
    success_url = reverse_lazy('dashboard:teacher:teacher_subject_groups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('dashboard:index')
        return redirect('login')


class DeleteTeacherSubjectGroup(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TeacherSubjectGroup
    success_url = reverse_lazy('dashboard:teacher:teacher_subject_groups')

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('dashboard:index')
        return redirect('login')


@user_passes_test(user_is_teacher_or_administrative)
def teacherSubjectView(request):
    teacher = Teacher.objects.get(teacher_account=request.user)
    # get student object
    # for showing subjects in option form
    teacher_subject_qs = TeacherSubjectGroup.objects.filter(
        teacher=teacher,
    )
    subjects = teacher_subject_qs
    context = {
        'teacher': teacher,
        'subjects': subjects,
    }
    return render(request, 'teacher/connect/teacher_subjects.html', context)


@user_passes_test(user_is_teacher_or_administrative)
def teacherStudentsView(request):
    teacher = Teacher.objects.get(teacher_account=request.user)
    ctx = {}
    if not request.GET:
        qs = TeacherSubjectGroup.objects.none()
    else:
        qs = TeacherSubjectGroup.objects.filter(teacher=teacher)

    subject_group_filter = TeacherSubjectGroupFilter(
        request.GET,
        queryset=qs
    )

    department = None
    for subject_group in subject_group_filter.qs:
        department = Department.objects.get(pk=subject_group.department.pk)
    ctx.update({
        'department': department,
    })

    students = Student.objects.filter(admission_student__choosen_department=department)

    ctx.update({
        'teacher': teacher,
        'subject_group_filter': subject_group_filter,
        'students': students

    })

    return render(request, 'teacher/connect/teacher_students.html', ctx)


@user_passes_test(user_is_teacher_or_administrative)
def teacherResultsView(request):
    teacher = Teacher.objects.get(teacher_account=request.user)
    ctx = {}
    if not request.GET:
        qs = TeacherSubjectGroup.objects.none()
    else:
        qs = TeacherSubjectGroup.objects.filter(teacher=teacher)

    subject_group_filter = TeacherSubjectGroupFilter(
        request.GET,
        queryset=qs
    )

    department = None
    subjects = None
    for subject_group in subject_group_filter.qs:
        department = Department.objects.get(pk=subject_group.department.pk)
        subjects = subject_group.subjects.all()
    ctx.update({
        'department': department,
    })
    students = Student.objects.filter(admission_student__choosen_department=department)

    print(subjects)

    if request.method == "POST":

        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data["subjects"]
                students = request.POST["students"]
                results = []
                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    for subject in subjects:
                        check = Result.objects.filter(
                            subject=subject,
                            student=stu,
                        ).first()
                        if not check:
                            results.append(
                                Result(
                                    subject=subject,
                                    student=stu,
                                )
                            )
                Result.objects.bulk_create(results)
                return redirect('dashboard:teacher:teacher_edit_results')
                # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "subjects": subjects
                }
            )
            form.fields['subjects'].queryset = subjects

            studentlist = ",".join(id_list)
            return render(
                request, "teacher/connect/teacher_results_entry2.html",
                {"students": studentlist, "form": form, "count": len(id_list),
                 'subject_group_filter': subject_group_filter},
            )
        else:
            messages.warning(request, "You didnt select any student.")
    ctx.update({
        'subject_group_filter': subject_group_filter,
        'students': students,
    })
    return render(request, 'teacher/connect/teacher_results_entry.html', ctx)


@login_required
def teacher_edit_results(request, **kwargs):
    teacher = Teacher.objects.get(teacher_account=request.user)
    ctx = {}
    if not request.GET:
        qs = TeacherSubjectGroup.objects.none()
    else:
        qs = TeacherSubjectGroup.objects.filter(teacher=teacher)

    subject_group_filter = TeacherSubjectGroupFilter(
        request.GET,
        queryset=qs
    )

    department = None
    subjects = None
    for subject_group in subject_group_filter.qs:
        department = Department.objects.get(pk=subject_group.department.pk)
        subjects = subject_group.subjects.all()
    ctx.update({
        'department': department,
    })
    students = Student.objects.filter(admission_student__choosen_department=department)

    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Résultats modifiés avec succès")
    else:
        results = Result.objects.filter(
            student__in=students, subject__in=subjects
        )
        form = EditResults(queryset=results)
    ctx.update({
        "formset": form,
        "subject_group_filter": subject_group_filter,
    })
    return render(request, "teacher/connect/teacher_edit_results.html", ctx)
