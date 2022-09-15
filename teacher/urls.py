from django.urls import path

from teacher.views import CreateTeacherView, TeacherListView, DeleteTeacherView, UpdateTeacherView, TeacherDetailView

app_name = 'teacher'


urlpatterns = [
    path('teacher/', TeacherListView.as_view(), name="read_teachers"),
    path('teacher/create/', CreateTeacherView.as_view(), name="create_teacher"),
    path('teacher/delete/<int:pk>', DeleteTeacherView.as_view(), name="delete_teacher"),
    path('teacher/edit/<int:pk>', UpdateTeacherView.as_view(), name="update_teacher"),
    path('teacher/details/<int:pk>', TeacherDetailView.as_view(), name="teacher_detail"),
]
