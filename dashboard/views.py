from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from academic.models import Department, AcademicSession, AcademicTerm
from permission_handlers.basic import user_is_verified
from student.models import Student
from teacher.models import Teacher


# Create your views here.
@user_passes_test(user_is_verified, login_url='permission_error')
def index(request):
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    total_students = Student.objects.count()
    current_session = AcademicSession.objects.get(current=True)
    current_term = AcademicTerm.objects.get(current=True)
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'current_session': current_session,
        'current_term': current_term,
    }
    return render(request, 'dashboard/index.html', context)


def header(request):
    current_session = AcademicSession.objects.get(current=True)
    current_term = AcademicTerm.objects.get(current=True)
    context = {
        'current_session': current_session,
        'current_term': current_term,
    }
    return render(request, 'includes/dashboard/navbar.html', context)
