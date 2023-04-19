from django.contrib import admin
from .models import Doctors, Category

# Register your models here.

admin.site.register(Doctors)
admin.site.register(Category)