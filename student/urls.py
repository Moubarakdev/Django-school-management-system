from datetime import datetime

from django.urls import path, register_converter

from student.forms import ApplicationForm1, ApplicationForm2, ApplicationForm3
from student.views.report_views import yearly_graph_api, counsel_monthly_report
from student.views.students_views import all_applicants, students_board, admitted_students_list, paid_registrants, \
    unpaid_registrants, rejected_registrants, admission_confirmation, admit_student, \
    mark_as_paid_or_unpaid, update_online_registrant, add_counseling_data, add_student_view, students_view, \
    StudentDetailsView, StudentUpdateView, student_delete_view, students_by_department_view, AlumnusListView, \
    ApplicationWizard, studentResultView, studentSubjectView, renew_admission, RegistrationDetails, reject_student

app_name = 'student'


class DateConverter:
    # Convert a string passed as date in datetime object
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'date')

urlpatterns = [
    path('', students_board, name='students_board'),
    path('add/', add_student_view, name='add_student'),
    path('all/', students_view, name='all_student'),
    path('alumnus/', AlumnusListView.as_view(), name='alumnus'),
    path('applicants/', all_applicants, name='all_applicants'),
    path('applicants/<int:pk>/detail', RegistrationDetails.as_view(), name='registration_details'),
    path('admitted-students/', admitted_students_list,
         name='admitted_student_list'),
    path('applicants/paid/', paid_registrants,
         name='paid_registrant_list'),
    path('applicants/unpaid/', unpaid_registrants, name='unpaid_registrant_list'),
    path('applicants/unpaid/mark-paid/', mark_as_paid_or_unpaid,
         name='mark_as_paid_or_unpaid'),
    path('add-counsel-data/<int:student_id>/', add_counseling_data,
         name='add_counseling_data'),
    path('rejected-registrants/', rejected_registrants,
         name='rejected_registrant_list'),
    path('update-registrant/<int:pk>/', update_online_registrant,
         name='update_online_registrant'),
    path('admission-confirm/', admission_confirmation,
         name='admission_confirmation'),
    path('online-applicants/<int:pk>/admit/', admit_student,
         name='admit_student'),
    path('online-applicants/<int:pk>/reject/', reject_student,
         name='reject_student'),

    path('new-admission/<int:pk>/admit/', renew_admission,
         name='new_admission'),

    path('update/<int:pk>/', StudentUpdateView.as_view(),
         name='update_student'),
    path('<int:pk>/detail/', StudentDetailsView.as_view(),
         name='student_details'),
    path('<int:pk>/delete/', student_delete_view, name='delete_student'),

    path('add-counsel-data/<int:student_id>/', add_counseling_data,
         name='add_counseling_data'),

    path('api/yearly-graph/', yearly_graph_api,
         name='yearly_graph_api'),

    path('counsel-report/', counsel_monthly_report, name='counsel_monthly_report'),
    path('counsel-report/<str:response_type>/', counsel_monthly_report,
         name='counsel_monthly_report_typed'),

    path('counsel-report/<str:response_type>/<date:date_param>/',
         counsel_monthly_report,
         name='counsel_report_monthly_with_date'),

    path('<int:pk>/students/', students_by_department_view,
         name='students_by_dept'),
    #
    path('application/', ApplicationWizard.as_view([ApplicationForm1, ApplicationForm2, ApplicationForm3]),
         name="application"),

    path('me/results', studentResultView, name="me_result"),
    path('me/subjects', studentSubjectView, name="me_subject"),

]
