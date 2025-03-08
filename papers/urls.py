from django.urls import path
from .views import signup, login, home

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
]
