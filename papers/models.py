from django.db import models

class UploadedExamPaper(models.Model):
    file = models.FileField(upload_to="temp/")  # Files are saved in media/temp/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
