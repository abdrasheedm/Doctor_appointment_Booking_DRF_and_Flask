from django.contrib import admin
from .models import Appointment, AppointmentBook

# Register your models here.

admin.site.register(Appointment)
admin.site.register(AppointmentBook)