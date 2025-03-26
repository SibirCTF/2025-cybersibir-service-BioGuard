from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BioGuard.urls')),
    path('profile', include('BioGuard.urls')),
    path('login', include('BioGuard.urls')),
    path('register', include('BioGuard.urls')),
]