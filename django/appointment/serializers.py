from rest_framework import serializers
from .models import Appointment, AppointmentBook
from doctors.serializers import GetDoctorSerializer
from datetime import datetime



class TimeSlotSerializer(serializers.ModelSerializer):
    doctor = GetDoctorSerializer()
    date = serializers.DateField(format='%A, %B %d')
    start_time = serializers.TimeField(format='%I:%M %p')
    end_time = serializers.TimeField(format='%I:%M %p')
    class Meta:
        model = Appointment
        fields = ['id', 'date','start_time', 'end_time', 'is_available', 'doctor']


class BookSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentBook
        fields = ['id' ,'user', 'appointment']


class BookedAppointmentSerializer(serializers.ModelSerializer):
    appointment = TimeSlotSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'appointment']

