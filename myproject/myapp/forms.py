from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class DoctorApplicationForm(forms.Form):
    specialty = forms.CharField(max_length=100)
    available_days = forms.CharField(max_length=100)  

