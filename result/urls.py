from django.urls import path

from result.views import result_view, result_detail_view, result_entry, create_subject_group, find_student, \
    subject_group_list

app_name = 'result'

urlpatterns = [
    path('', result_view, name='index'),
    path('student/<int:student_pk>/', result_detail_view, name='result_detail_view'),
    path('entry/', result_entry, name='result_entry'),
    path('create-subject-group/', create_subject_group, name='create_subject_group'),
    path('subject-groups/', subject_group_list, name='subject_groups'),
    path('student/find/<str:student_id>', find_student, name='find_student'),
]
