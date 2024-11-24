from users.apps import UsersConfig
from django.urls import path, include

from users.views import register

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
]

