from datetime import date


from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from rolepermissions.roles import assign_role

from academic.models import Department, Subject
from permission_handlers.administrative import user_is_admin_su_or_ac_officer, user_is_teacher_or_administrative
from permission_handlers.basic import user_is_verified
from result.filters import SubjectGroupFilter
from result.models import SubjectGroup
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
