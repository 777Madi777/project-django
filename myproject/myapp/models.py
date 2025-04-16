from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)

    username = None 
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name']  

    def __str__(self):
        return self.email
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    available_days = models.CharField(max_length=100)

class Appointment(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # исправлено
    date = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    @property
    def time(self):
        return self.date.strftime('%H:%M')

