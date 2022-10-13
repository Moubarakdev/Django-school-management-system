from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from academic.models import Subject, Department
from permission_handlers.administrative import user_is_teacher_or_administrative
from permission_handlers.basic import user_is_verified
from result.filters import ResultFilter, SubjectGroupFilter
from result.forms import SubjectGroupForm, ResultForm
from result.models import Result, SubjectGroup
from student.models import Student


@user_passes_test(user_is_verified)
# Create your views here.
def result_view(request):
    if not request.GET:
        qs = Result.objects.none()
    else:
        qs = Result.objects.all()
    f = ResultFilter(request.GET, queryset=qs)
    ctx = {'filter': f, }
    return render(request, 'result/result_filter.html', ctx)


@user_passes_test(user_is_verified)
def result_detail_view(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    student_results = student.results.all()
    departments = list(Department.objects.all())
    department_results = {}
    active_departments = []

    for department in departments:
        results = student_results.filter(choosen_department=department)
        if results:
            active_departments.append(department)
            department_results.update(
                {f'{department}': results}
            )
    ctx = {
        'student': student,
        'department_results': department_results,
        'active_departments': active_departments
    }
    return render(request, 'result/result_detail.html', ctx)


def find_student(request, student_id):
    """ Find student by given id for result entry."""
    student = Student.objects.get(
        temporary_id=student_id
    )
    ctx = {
        'student_name': student.admission_student.last_name,
        'student_first_name': student.admission_student.first_name,
        'student_department': student.admission_student.choosen_department,
        'image_url': student.admission_student.photo.url
    }
    return JsonResponse({'data': ctx})


@user_passes_test(user_is_teacher_or_administrative)
def result_entry(request):
    if not request.GET:
        qs = SubjectGroup.objects.none()
    else:
        qs = SubjectGroup.objects.all()

    subject_group_filter = SubjectGroupFilter(
        request.GET,
        queryset=qs
    )

    if request.method == 'POST':
        data_items = request.POST.items()
        # get student from pk
        student_temp_id = request.POST.get('student_id')
        student = Student.objects.get(temporary_id=student_temp_id)

        result_created = {}
        for key, value in data_items:
            # get subject from pk
            if '.' in key:
                try:
                    s_pk = int(key.split('.')[1])
                    subject = Subject.objects.get(pk=s_pk)
                    if not result_created.get(str(s_pk)):
                        # get subject marks
                        class_marks = int(
                            request.POST.get(f'class_marks.{s_pk}')
                        )
                        exam_marks = int(
                            request.POST.get(f'exam_marks.{s_pk}')
                        )
                        extra_marks = int(
                            request.POST.get(f'extra_marks.{s_pk}')
                        )
                        result = Result(
                            student=student,
                            subject=subject,
                            class_marks=class_marks,
                            exam_marks=exam_marks,
                            extra_marks=extra_marks,
                        )
                        try:
                            result.save()
                            result_created[str(s_pk)] = True
                        except IntegrityError:
                            messages.error(
                                request,
                                f'Les notes de {student.admission_student.last_name}\' dans la matière '
                                f' {subject} ont déjà été saisis.'
                            )
                except ValueError:
                    pass
        return redirect('result:result_entry')
    ctx = {
        'subject_group_filter': subject_group_filter,
    }
    return render(request, 'result/result_entry.html', ctx)


@user_passes_test(user_is_teacher_or_administrative)
def create_subject_group(request):
    departments = Department.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        dept_pk = int(request.POST.get('department'))
        subject_list = request.POST.getlist('subject')

        dept = Department.objects.get(pk=dept_pk)

        subject_group = SubjectGroup.objects.create(
            department=dept,
        )

        subject_objects = []
        for s_pk in subject_list:
            subj = Subject.objects.get(pk=int(s_pk))
            subject_objects.append(subj)
            subject_group.subjects.add(subj)

        subject_group.save()
        return redirect('result:subject_groups')
    ctx = {
        'departments': departments,
        'subjects': subjects,
    }
    return render(request, 'result/create_subject_groups.html', ctx)


@user_passes_test(user_is_verified)
def subject_group_list(request):
    subject_groups = SubjectGroup.objects.all()
    ctx = {
        'subject_groups': subject_groups,
    }
    return render(request, 'result/subject_group_list.html', ctx)


class UpdateSubjectGroup(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubjectGroup
    form_class = SubjectGroupForm
    template_name = 'result/subject_group_form.html'
    success_url = reverse_lazy('result:subject_groups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')


class UpdateResultView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Result
    form_class = ResultForm
    template_name = 'result/result_form.html'
    success_url = reverse_lazy('result:result_filter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')


class DeleteResultView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Result
    form_class = ResultForm
    template_name = 'result/result_form.html'
    success_url = reverse_lazy('result:result_filter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['button'] = "Modifier"
        return context

    def test_func(self):
        user = self.request.user
        return user_is_teacher_or_administrative(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')
