from django.urls import path

from teacher.views import CreateTeacherView, TeacherListView, DeleteTeacherView, UpdateTeacherView, TeacherDetailView, \
    TeacherApplication, all_applicants, admit_teacher, create_teacher_subject_group, teacher_subject_group_list, \
    UpdateTeacherSubjectGroup, DeleteTeacherSubjectGroup

app_name = 'teacher'

urlpatterns = [
    path('teacher/', TeacherListView.as_view(), name="read_teachers"),
    path('teacher/applicants', all_applicants, name="teacher_applicants"),
    path('teacher/create/', CreateTeacherView.as_view(), name="create_teacher"),
    path('teacher/delete/<int:pk>', DeleteTeacherView.as_view(), name="delete_teacher"),
    path('teacher/edit/<int:pk>', UpdateTeacherView.as_view(), name="update_teacher"),
    path('teacher/details/<int:pk>', TeacherDetailView.as_view(), name="teacher_detail"),
    path('teacher/application', TeacherApplication.as_view(), name="teacher_application"),
    path('teacher-applicants/<int:pk>/admit/', admit_teacher, name='admit_teacher'),

    path('create-subject-group/', create_teacher_subject_group, name='create_teacher_subject_group'),
    path('subject-groups/', teacher_subject_group_list, name='teacher_subject_groups'),
    path('subject-groups/update/<int:pk>', UpdateTeacherSubjectGroup.as_view(), name='update_teacher_subject_groups'),
    path('subject-groups/delete/<int:pk>', DeleteTeacherSubjectGroup.as_view(), name='delete_teacher_subject_groups'),
]
