from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from academic.models import Department
from permission_handlers.basic import user_is_verified
from student.models import Student
from teacher.models import Teacher


# Create your views here.
@user_passes_test(user_is_verified, login_url='permission_error')
def index(request):
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    total_students = Student.objects.count()
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
    }
    return render(request, 'dashboard/index.html', context)
