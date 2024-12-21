# images/models.py
from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at}"
    
class VisitorPass(models.Model):
    visitor_name = models.CharField(max_length=50)
    date_of_birth = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    purpose = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=5)
    duration = models.CharField(max_length=5)
    authorized_by = models.CharField(max_length=50)
    qr_img_name = models.CharField(max_length=50)
    pass_id = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    def __str__(self):
        return self.pass_id
