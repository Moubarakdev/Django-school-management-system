from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from academic.forms import DepartmentForm, SemesterForm, AcademicSessionForm, SubjectForm, BatchForm
from academic.models import Department, Semester, Subject, AcademicSession, Batch
from permission_handlers.administrative import user_is_admin_su_editor_or_ac_officer, user_editor_admin_or_su, \
    user_is_teacher_or_administrative
from permission_handlers.basic import user_is_verified


# Create your views here.

# #### SEMESTER #############################################
class ReadSemester(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Semester
    context_object_name = 'semesters'
    template_name = 'semester/semester_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)


class CreateSemester(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'semester/semester_form.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_semesters')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateSemester(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Semester
    form_class = SemesterForm

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    template_name = 'semester/semester_form.html'


class DeleteSemester(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Semester
    template_name = 'semester/batch_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_semesters')

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)


# #### SUBJECT #############################################
class SubjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'subject/subject_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)


class CreateSubjectView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject/subject_form.html'

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_subjects')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateSubjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject/subject_form.html'

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:academic:read_subjects')


class DeleteSubjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Subject
    template_name = 'subject/subject_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_subjects')

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)


# ########## DEPARTMENT ###################
class CreateDepartmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Department
    form_class = DepartmentForm

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_departments')
    template_name = 'department/department_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateDepartmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department/department_form.html'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:academic:read_departments')


class DepartmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Department
    context_object_name = "departments"
    template_name = 'department/department_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)


class DeleteDepartmentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Department
    template_name = 'department/department_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_departments')

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)


# #################################

class CreateAcademicSession(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_academic_sessions')
    template_name = 'academic/academic_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class AcademicSessionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AcademicSession
    context_object_name = "ac_sessions"
    template_name = 'academic/academic_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)


class UpdateAcademicSession(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:academic:read_ac_sessions')
    template_name = 'academic/academic_form.html'


class DeleteAcademicSession(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AcademicSession
    template_name = 'academic/academic_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_ac_sessions')

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)


# ########## BATCH ###################
class CreateBatchView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Batch
    form_class = BatchForm

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_batches')
    template_name = 'batch/batch_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateBatchView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'batch/batch_form.html'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:academic:read_batches')


class BatchListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Batch
    context_object_name = "batches"
    template_name = 'batch/batch_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)


class DeleteBatchView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Batch
    template_name = 'batch/batch_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_batches')

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)

# #################################
