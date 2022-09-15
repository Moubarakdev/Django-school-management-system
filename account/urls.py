from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from django_countries import settings

from account.views import login_view, profile_complete, register, profile_picture_upload, user_approval, \
    user_approval_with_modification, AccountListView, UserUpdateView

app_name = 'account'

urlpatterns = [
                  path('', profile_complete, name='profile_complete'),
                  path('login/', login_view, name="login"),
                  path('signup/', register, name="register"),
                  path('logout/', LogoutView.as_view(), name="logout"),
                  path('accounts/', AccountListView.as_view(), name='read_accounts'),
                  path('account/create/<int:pk>', UserUpdateView.as_view(), name='update_account'),
                  path('approval/<int:pk>/<int:approved>', user_approval, name='user_approval'),
                  path('modify-and-approve/<int:pk>/', user_approval_with_modification,
                       name='approval_with_modification'),
                  path('api/upload-profile-picture', profile_picture_upload, name='profile_picture_upload'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
