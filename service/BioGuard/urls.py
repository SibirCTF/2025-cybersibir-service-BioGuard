from django.urls import path
from . import views

urlpatterns = [
    path('', views.bioguard_info, name='bioguard_info'),
    path('profile', views.profile, name='profile'),
    path('appointment', views.appointment, name='appointment'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('register/staff', views.register_staff, name='register'),
    path('service/add', views.create_service, name='service'),
    path('service/get', views.get_service, name='service'),
]