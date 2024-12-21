from django.db import models

class Identity(models.Model):
    id = models.AutoField(primary_key=True)
    # GENDER_CHOICES - [('M','Male'), ('F','Female'), ('O':'Other')]
    name = models.CharField(max_length=250)
    pan = models.CharField(max_length=10, unique=True, blank=True, null=True)
    aadhaar = models.CharField(max_length=16, unique=True, blank=True, null=True)
    dob = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    # gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # phone = models.CharField(max_length=10, blank=True, null=True)
    # email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='identities', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'identities'