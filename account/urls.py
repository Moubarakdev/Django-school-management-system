from django.urls import path

from account.views import login_view, profile_complete, register

app_name = 'account'

urlpatterns = [
    path('', profile_complete, name='profile_complete'),
    path('login/', login_view, name="login"),
    path('signup/', register, name="register")
]
