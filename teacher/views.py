from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

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
