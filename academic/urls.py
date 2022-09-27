from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from academic.views import ReadSemester, CreateSemester, DeleteSemester, UpdateSemester, SubjectListView, \
    CreateSubjectView, UpdateSubjectView, DeleteSubjectView, CreateDepartmentView, UpdateDepartmentView, \
    DeleteDepartmentView, CreateAcademicSession, AcademicSessionListView, DepartmentListView, DeleteAcademicSession, \
    UpdateAcademicSession, CreateBatchView, DeleteBatchView, UpdateBatchView, BatchListView
from myschool import settings

app_name = 'academic'

urlpatterns = [
                  # Semester
                  path('semester/', ReadSemester.as_view(), name="read_semesters"),
                  path('semester/create/', CreateSemester.as_view(), name="create_semester"),
                  path('semester/delete/<int:pk>', DeleteSemester.as_view(), name="delete_semester"),
                  path('semester/edit/<int:pk>', UpdateSemester.as_view(), name="update_semester"),

                  # Subject
                  path('subject/', SubjectListView.as_view(), name="read_subjects"),
                  path('subject/create/', CreateSubjectView.as_view(), name="create_subject"),
                  path('subject/delete/<int:pk>', DeleteSubjectView.as_view(), name="delete_subject"),
                  path('subject/edit/<int:pk>', UpdateSubjectView.as_view(), name="update_subject"),

                  # Department
                  path('department/', DepartmentListView.as_view(), name="read_departments"),
                  path('department/create/', CreateDepartmentView.as_view(), name="create_department"),
                  path('department/delete/<int:pk>', DeleteDepartmentView.as_view(), name="delete_department"),
                  path('department/edit/<int:pk>', UpdateDepartmentView.as_view(), name="update_department"),

                  # Academic Session
                  path('academicsession/', AcademicSessionListView.as_view(), name="read_ac_sessions"),
                  path('academicsession/create/', CreateAcademicSession.as_view(), name="create_ac_session"),
                  path('academicsession/delete/<int:pk>', DeleteAcademicSession.as_view(), name="delete_ac_session"),
                  path('academicsession/update/<int:pk>', UpdateAcademicSession.as_view(), name="update_ac_session"),

                  # Batch
                  path('batch/', BatchListView.as_view(), name="read_batches"),
                  path('batch/create/', CreateBatchView.as_view(), name="create_batch"),
                  path('batch/delete/<int:pk>', DeleteBatchView.as_view(), name="delete_batch"),
                  path('batch/update/<int:pk>', UpdateBatchView.as_view(), name="update_batch"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
