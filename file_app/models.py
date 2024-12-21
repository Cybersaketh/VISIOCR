from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    title = models.CharField(max_length=200, null=True, default=None)
    file = models.FileField(upload_to="uploads/")
 
    def __str__(self):
        return self.title