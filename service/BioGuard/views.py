from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Appointment, Service
from .forms import UserRegisterForm, LoginForm, PatientForm, StaffForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dataclasses import dataclass
import logging


@dataclass
class BookedDate:
    date : str
    person : str
    service : Service

bDates = []


def bioguard_info(request):
    return render(request, 'BioGuard/index.html', {})


@login_required
def profile(request):
    if not hasattr(request.user, 'patient'):
        return HttpResponse("This patient does not exist!")
    patient = Patient.objects.filter(username=request.user.username).get()
    return render(request, 'BioGuard/profile.html', {'patient': patient})
        

@login_required
def appointment(request):
    services = Service.objects.all()
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        service_id = request.POST.get('service')
        service = services.filter(id = service_id).get()
        if bDates:
            for b in bDates:
                if b.date == appointment_date and b.service.id == service_id:
                    messages.error(request, f'This temporary booked! Try later.')
                    return render(request, 'BioGuard/appointment.html', {'services': services})
        bDates.append(BookedDate(appointment_date, request.user.username, service))
        patient = request.user.patient
        p = Patient.objects.filter(username=request.user.username).get()     
        try:
            if appointment_date >= str(timezone.now().date()): 
                if not p.vip and service.vip :
                    messages.error(request, f'This service is only for vip!')
                    return render(request, 'BioGuard/appointment.html', {'services': services})
                service = bDates.pop()
                appointment = Appointment(date=service.date, username=patient,service_id=service.service)
                appointment.save()
                p.appointments = str(p.appointments).replace("None","") + f' {service.date} - {service.service.name} ({   service.service.description.replace("None","")});'
                p.save()
                messages.success(request, f'Appointment created!')
                return redirect('/profile')
        except Exception as e:
            # logging.error(e)
            messages.error(request, f'Invalid appointment!')
    return render(request, 'BioGuard/appointment.html', {'services': services})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(request.user, 'patient'):
                    return redirect('/profile')
                else:
                    return HttpResponse("Successful login", status=200)
            else:
                messages.error(request, f'Invalid username or password!')
        else:
            messages.error(request, f'Invalid username or password!')
    else:
        form = LoginForm()
    return render(request, 'BioGuard/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        patient_form = PatientForm(request.POST)
        if form.is_valid() and patient_form.is_valid():
            user = form.save()

            patient = patient_form.save(commit=False)
            patient.user = user

            patient.save()
            messages.success(request, f'Account created!')
            return redirect('/login')
        else:
            messages.error(request, f'Invalid username or password!')
    else:
        form = UserRegisterForm()
    return render(request, 'BioGuard/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')

def register_staff(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        staff_form = StaffForm(request.POST)
        if form.is_valid() and staff_form.is_valid():
            user = form.save()

            staff = staff_form.save(commit=False)
            staff.user = user

            staff.save()
            return HttpResponse("Account created!")
        else:
            return HttpResponse("Invalid username or password!")
        
@login_required
def create_service(request):
    if request.method == 'POST':
        try:
            if not hasattr(request.user, 'staff'):
                return HttpResponse("You do not have permission to create a service!", status=403)
            name = request.POST.get('name')
            description = request.POST.get('description', None)
            vip = request.POST.get('vip', False)
            if not name:
                print("Name is required")
                return HttpResponse("Name is required!", status=400)
            Service.objects.create(
                name=name,
                description=description,
                vip=bool(vip)
            )
            return HttpResponse("Service created!", status=201)
        except:
            return HttpResponse("Error creating service!", status=500)
        
# def docs_view(request):
#     if request.method == 'TRACE':
#         response = HttpResponse("This is a TRACE response.")
#         response['Content-Type'] = 'text/plain'
#         return response
#     else:
#         return HttpResponseNotAllowed(['TRACE'])


# def profiles(request):
#     username = request.GET.get('user')
#     if not username:
#         patient = request.user.patient
#     else:
#         user = get_object_or_404(User, username=username)
#         patient = get_object_or_404(Patient, user=user)
#     return render(request, 'BioGuard/profile.html', {'patient': patient})