from django.db import models
from doctors.models import Doctors
from account.models import Account

# Create your models here.

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField(default='2023-02-09')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.doctor} : {self.start_time} - {self.end_time}"
    


class AppointmentBook(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.appointment}"
    
    def save(self,*args, **kwargs):
        self.appointment.is_available = False
        self.appointment.save()
        super(AppointmentBook, self).save(*args, **kwargs)
