from django import forms
from .models import UploadedExamPaper

class ExamPaperUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedExamPaper
        fields = ["file"]