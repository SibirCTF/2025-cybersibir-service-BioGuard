from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    # username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    diagnosis = models.CharField(max_length=300, blank=True, null=True)
    appointments = models.CharField(max_length=300, blank=True, null=True)
    vip = models.BooleanField(default=False)

    # def __str__(self):
    #     return f'Name: {self.first_name} {self.last_name}, Birth Year: {self.birth_year}, Email: {self.email}'


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    vip = models.BooleanField(default=False) 

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=2997-12-12)
    username = models.ForeignKey(Patient, on_delete=models.CASCADE, to_field="username")
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['date', 'service_id'], name='unique_appointment')
        ]

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    username = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
# class User(models.Model):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     birth_year = models.IntegerField(max_length=30, blank=True)
#     password = models.CharField()

#     USERNAME_FIELD = 'email'

#     def __str__(self):
#         return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
