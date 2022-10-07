from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from payment.forms import SchoolFeesForm
from payment.models import SchoolFees
from permission_handlers.administrative import user_is_admin_su_editor_or_ac_officer


# Create your views here.
class FeesCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SchoolFees
    form_class = SchoolFeesForm

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Créer"
        return context

    success_url = reverse_lazy('payment:read_fees')
    template_name = 'fees/fees_form.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class FeesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SchoolFees
    context_object_name = "fees"
    template_name = 'fees/fees_list.html'

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)


class FeesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SchoolFees
    form_class = SchoolFeesForm

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    success_url = reverse_lazy('payment:read_fees')
    template_name = 'fees/fees_form.html'


class FeesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SchoolFees
    context_object_name = 'fee'
    template_name = 'fees/fees_confirm_delete.html'
    success_url = reverse_lazy('payment:read_fees')

    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)
