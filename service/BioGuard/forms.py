from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Appointment, Service, Staff


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'password1' : forms.PasswordInput()
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['username', 'first_name', 'last_name', 'birth_year', 'email', 'diagnosis', 'appointments', 'vip']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'username', 'service_id']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['id', 'name', 'specialist', 'description', 'vip']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['username', 'first_name', 'last_name', 'position']