from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from academic.forms import DepartmentForm, AcademicSessionForm, SubjectForm, SiteConfigForm, \
    CurrentSessionForm
from academic.models import Department, Subject, AcademicSession, SiteConfig
from permission_handlers.administrative import user_is_admin_su_editor_or_ac_officer, user_editor_admin_or_su, \
    user_is_teacher_or_administrative
from permission_handlers.basic import user_is_verified

# Create your views here.

# #### SEMESTER #############################################

'''
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
'''


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
    context_object_name = 'subject'
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
    context_object_name = 'department'
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

    success_url = reverse_lazy('dashboard:academic:read_ac_sessions')
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

    def form_valid(self, form):
        obj = self.object
        if not obj.current:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("dashboard:academic:read_ac_sessions")
        return super().form_valid(form)


class DeleteAcademicSession(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AcademicSession
    context_object_name = 'ac_session'
    template_name = 'academic/academic_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_ac_sessions')

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("dashboard:academic:read_ac_sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(DeleteAcademicSession, self).delete(request, *args, **kwargs)


# ########## BATCH ###################
'''class CreateBatchView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
    context_object_name = 'batch'
    template_name = 'batch/batch_confirm_delete.html'
    success_url = reverse_lazy('dashboard:academic:read_batches')

    def test_func(self):
        user = self.request.user
        return user_editor_admin_or_su(user)
'''


# #################################

class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "site/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


# ############################## TERMS ########################
'''class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    context_object_name = 'terms'
    template_name = "term/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context


class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "term/term_form.html"
    success_url = reverse_lazy("dashboard:academic:read_terms")
    success_message = "New term successfully added"
'''

'''class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("dashboard:academic:read_terms")
    success_message = "Term successfully updated."
    template_name = "term/term_form.html"

    def form_valid(self, form):
        obj = self.object
        if not obj.current:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
        return super().form_valid(form)'''

"""class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("dashboard:academic:read_terms")
    template_name = "term/term_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("read_terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)

"""


# ####################### CURENT ##########################
class CurrentSessionAndTermView(LoginRequiredMixin, View, UserPassesTestMixin):
    """Current Session and Term"""
    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    form_class = CurrentSessionForm
    template_name = "current/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                # "current_term": AcademicTerm.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["session_courante"].year
            AcademicSession.objects.filter(year=session).update(current=True)
            AcademicSession.objects.exclude(year=session).update(current=False)
            '''AcademicTerm.objects.filter(name=term).update(current=True)
            AcademicTerm.objects.exclude(name=term).update(current=False)'''

        return render(request, self.template_name, {"form": form})
