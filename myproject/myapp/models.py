from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_doctor', False)
        extra_fields.setdefault('is_patient', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)

    username = None 
    email = models.EmailField(unique=True)  

    gender_choices = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialty}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    @property
    def time(self):
        return self.date.strftime('%H:%M')

    def __str__(self):
        return f"{self.patient.email} → {self.doctor.user.email} @ {self.date}"