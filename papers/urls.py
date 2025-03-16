from django.urls import path
from .views import signup, login, dashboard, logout, paper_builder, generated_paper

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout, name="logout"),
    path("paper_builder/", paper_builder, name="paper_builder"),
    path("generated_paper/", generated_paper, name="generated_paper"),
]
