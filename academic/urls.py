from django.contrib import admin
from django.urls import path, include

from academic.views import ReadSemester, CreateSemester, DeleteSemester, UpdateSemester, SubjectListView, \
    CreateSubjectView, UpdateSubjectView, DeleteSubjectView, CreateDepartmentView, UpdateDepartmentView, \
    DeleteDepartmentView, CreateAcademicSession

app_name = 'academic'

urlpatterns = [

    # Semester
    path('semester/', ReadSemester.as_view(), name="read_semesters"),
    path('semester/create/', CreateSemester.as_view(), name="create_semester"),
    path('semester/delete/<int:semester_id>', DeleteSemester.as_view(), name="delete_semester"),
    path('semester/edit/<int:semester_id>', UpdateSemester.as_view(), name="update_semester"),

    # Subject
    path('subject/', SubjectListView.as_view(), name="read_subjects"),
    path('subject/create/', CreateSubjectView.as_view(), name="create_subject"),
    path('subject/delete/<int:subject_id>', DeleteSubjectView.as_view(), name="delete_subject"),
    path('subject/edit/<int:subject_id>', UpdateSubjectView.as_view(), name="update_subject"),

    # Department
    path('department/', SubjectListView.as_view(), name="read_departments"),
    path('department/create/', CreateDepartmentView.as_view(), name="create_department"),
    path('department/delete/<int:department_id>', DeleteDepartmentView.as_view(), name="delete_department"),
    path('department/edit/<int:department_id>', UpdateDepartmentView.as_view(), name="update_department"),

    # Academic Session
    path('academicsession/', AcademicSessionListView.as_view(), name="read_academic_sessions"),
    path('academicsession/create/', CreateAcademicSession.as_view(), name="create_ac_session"),
]
