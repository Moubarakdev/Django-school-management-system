from django.urls import path, include

from account.views import UserRequestsListView
from dashboard.views import index, studentIndex, TeacherIndex

app_name = "dashboard"

urlpatterns = [
    path('', index, name="index"),
    path('stdash', studentIndex, name="student_dash"),
    path('tdash', TeacherIndex, name="teacher_dash"),
    path('academic/', include('academic.urls')),
    path('requests/', UserRequestsListView.as_view(), name="read_requests"),
    path('students/', include('student.urls')),
    path('teachers/', include('teacher.urls')),
]
