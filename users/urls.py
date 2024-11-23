from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LogoutView, LoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]