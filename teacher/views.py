from datetime import date

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from rolepermissions.roles import assign_role

from permission_handlers.administrative import user_is_admin_su_or_ac_officer
from teacher.forms import TeacherForm
from teacher.models import Teacher


# Create your views here.
class CreateTeacherView(CreateView):
    model = Teacher
    form_class = TeacherForm

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


class UpdateTeacherView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teacher/teacher_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('dashboard:teacher:read_teachers')


class TeacherListView(ListView):
    model = Teacher
    queryset = Teacher.objects.filter(assigned_as_teacher=True)
    context_object_name = "teachers"
    template_name = 'teacher/teacher_list.html'


class DeleteTeacherView(DeleteView):
    model = Teacher
    template_name = 'teacher/teacher_confirm_delete.html'
    success_url = reverse_lazy('dashboard:teacher:read_teachers')


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teacher/teacher_detail.html'
    context_object_name = 'teacher'


class TeacherApplication(CreateView):
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
