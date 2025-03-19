from django.urls import path
from .views import signup, login, dashboard, logout, paper_builder, generate_exam_paper, download_exam_paper

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout, name="logout"),
    path("paper-builder/", paper_builder, name="paper_builder"),
    path("generate-exam-paper/", generate_exam_paper, name="generate_exam_paper"),
    path("download-exam-paper/", download_exam_paper, name="download_exam_paper"),
]
