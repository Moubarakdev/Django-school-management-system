from datetime import timedelta

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.utils import timezone

from academic.models import Department, AcademicSession, Subject
from permission_handlers.basic import user_is_verified
from result.models import Result, SubjectGroup
from student.models import Student, AdmissionStudent
from teacher.models import Teacher, TeacherSubjectGroup


# Create your views here.
# @user_passes_test(user_is_verified, login_url='permission_error')
@login_required
def index(request):
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    total_students = AdmissionStudent.objects.filter(assigned_as_student=True).values('last_name',
                                                                                      'first_name').distinct().count()
    current_session = AcademicSession.objects.get(current=True)
    # current_term = AcademicTerm.objects.get(current=True)
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'current_session': current_session,
    }

    today = timezone.localtime(timezone.now())
    history1 = today - timedelta(days=360)
    history2 = today - timedelta(days=360 * 2)
    history3 = today - timedelta(days=360 * 3)

    values = []
    dataBoys = []
    dataGirls = []
    studentsB1 = AdmissionStudent.objects.filter(gender="M", assigned_as_student=True,
                                                 created__range=(history3, today)).values('last_name',
                                                                                          'first_name').distinct().count()
    studentsG1 = AdmissionStudent.objects.filter(gender="F", assigned_as_student=True,
                                                 created__range=(history3, today)).values('last_name',
                                                                                          'first_name').distinct().count()

    values.append(today.year)
    dataGirls.append(studentsG1)
    dataBoys.append(studentsB1)

    studentsB2 = AdmissionStudent.objects.filter(gender="M", assigned_as_student=True,
                                                 created__range=(history3, history2)).values('last_name',
                                                                                             'first_name').distinct().count()
    studentsG2 = AdmissionStudent.objects.filter(gender="F", assigned_as_student=True,
                                                 created__range=(history3, history2)).values('last_name',
                                                                                             'first_name').distinct().count()

    values.append(history2.year)
    dataGirls.append(studentsG2)
    dataBoys.append(studentsB2)

    studentsB3 = AdmissionStudent.objects.filter(gender="M", assigned_as_student=True,
                                                 created__range=(history2, history1)).values('last_name',
                                                                                             'first_name').distinct().count()
    studentsG3 = AdmissionStudent.objects.filter(gender="F", assigned_as_student=True,
                                                 created__range=(history2, history1)).values('last_name',
                                                                                             'first_name').distinct().count()

    values.append(history3.year)
    dataGirls.append(studentsG3)
    dataBoys.append(studentsB3)

    context['values'] = values
    context['dataGirls'] = dataGirls
    context['dataBoys'] = dataBoys

    if request.user.requested_role == "admin" or request.user.requested_role == "academic_officer" or request.user.requested_role == 'accounts':
        return render(request, 'dashboard/index.html', context)
    elif request.user.requested_role == "teacher":
        ctx = {

        }
        try:
            teacher = Teacher.objects.get(teacher_account=request.user)
            subjects_g = TeacherSubjectGroup.objects.filter(
                teacher=teacher, ac_session=request.current_session
            )
            nb_depts = 0
            nb_students = 0
            nb_hours = 0
            for subject_g in subjects_g:
                subjects = subject_g.subjects.all()
                for subject in subjects:
                    hours = Subject.objects.get(subject_code=subject.subject_code).hourly_volume
                    nb_hours += hours
                if subject_g.department:
                    students = Student.objects.filter(
                        admission_student__choosen_department=subject_g.department).count()
                    nb_students += students
                    nb_depts += 1

            ctx = {
                'subjects': subjects_g,
                'nb_depts': nb_depts,
                'nb_students': nb_students,
                'nb_hours': nb_hours,
            }
        except:
            pass
        return render(request, 'dashboard/teacher_dashboard.html', ctx)
    else:
        ctx = {

        }
        try:
            student = Student.objects.get(admission_student__student_account=request.user)
            vresults = Result.objects.filter(validated=True, finished=True, student=student)
            nresults = Result.objects.filter(validated=False, finished=True, student=student)
            subjects = SubjectGroup.objects.get(department=student.admission_student.choosen_department).subjects

            ctx = {
                'vresults': vresults,
                'nresults': nresults,
                'subjects': subjects,
            }
        except:
            pass

        return render(request, 'dashboard/student_dashboard.html', ctx)


@login_required
def studentIndex(request):
    return render(request, 'dashboard/student_dashboard.html')


@login_required
def TeacherIndex(request):
    return render(request, 'dashboard/teacher_dashboard.html')
