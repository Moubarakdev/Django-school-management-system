from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from django_countries import settings

from account.views import login_view, profile_complete, register, profile_picture_upload, user_approval, \
    user_approval_with_modification, AccountListView, UserUpdateView, CreateUserView, ChangePasswordView
from permission_handlers.basic import permission_error

# app_name = 'account'

urlpatterns = [
                  path('profile/', profile_complete, name='profile_complete'),
                  path('login/', login_view, name="login"),
                  path('signup/', register, name="register"),
                  path('logout/', LogoutView.as_view(), name="logout"),
                  path('verification/', include('verify_email.urls')),
                  path('accounts/', AccountListView.as_view(), name='read_accounts'),
                  path('account/update/<int:pk>', UserUpdateView.as_view(), name='update_account'),
                  path('account/create/', CreateUserView.as_view(), name='create_account'),
                  path('approval/<int:pk>/<int:approved>', user_approval, name='user_approval'),
                  path('modify-and-approve/<int:pk>/', user_approval_with_modification,
                       name='approval_with_modification'),
                  path('api/upload-profile-picture', profile_picture_upload, name='profile_picture_upload'),
                  path('permission-error/', permission_error, name='permission_error'),
                  # Password reset urls ##############################################################################
                  path('reset_password/', PasswordResetView.as_view(template_name="account/password_reset.html"),
                       name="reset_password"),
                  path('reset_password_sent/',
                       PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"),
                       name="password_reset_done"),
                  path('reset/<uidb64>/<token>/',
                       PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"),
                       name="password_reset_confirm"),
                  path('reset_password_complete/',
                       PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
                       name="password_reset_complete"),

                  path('password-change/', ChangePasswordView.as_view(), name='password_change'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
