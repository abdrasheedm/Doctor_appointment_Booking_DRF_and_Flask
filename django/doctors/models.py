from django.db import models
from account.models import Account

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.category


class Doctors(models.Model):
    doctor = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.doctor.first_name} - {self.category.category}"
    
