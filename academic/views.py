from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from academic.forms import DepartmentForm, SemesterForm, AcademicSessionForm, SubjectForm
from academic.models import Department, Semester, Subject, AcademicSession


# Create your views here.

# #### SEMESTER #############################################
class ReadSemester(ListView):
    model = Semester
    context_object_name = 'semesters'
    template_name = 'semester/semester_list.html'


class CreateSemester(CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'semester/semester_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_semesters')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateSemester(UpdateView):
    model = Semester
    form_class = SemesterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    template_name = 'semester/semester_form.html'


class DeleteSemester(DeleteView):
    model = Semester
    template_name = 'semester/batch_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_semesters')


# #### SUBJECT #############################################
class SubjectListView(ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'subject/subject_list.html'


class CreateSubjectView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject/subject_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('dashboard:academic:read_subjects')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateSubjectView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject/subject_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:academic:read_subjects')


class DeleteSubjectView(DeleteView):
    model = Subject
    template_name = 'subject/subject_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_subjects')


# ########## DEPARTMENT ###################"
class CreateDepartmentView(CreateView):
    model = Department
    form_class = DepartmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('academic:read_departments')
    template_name = 'department/department_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateDepartmentView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academic/department_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:academic:read_departments')


class DepartmentListView(ListView):
    model = Department
    context_object_name = "departments"
    template_name = 'department/department_list.html'


class DeleteDepartmentView(DeleteView):
    model = Department
    template_name = 'department/department_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_departments')


# #################################

class CreateAcademicSession(CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm

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


class AccademicSessionListView(ListView):
    model = AcademicSession
    context_object_name = "ac_sessions"
    template_name = 'academic/academic_list.html'
