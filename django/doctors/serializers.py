from rest_framework import serializers
from .models import Category, Doctors
from account.serializer import SignUpSerializer


class CategoryLIstSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GetDoctorSerializer(serializers.ModelSerializer):
    doctor = SignUpSerializer()
    category = CategoryLIstSerializer()
    class Meta:
        model = Doctors
        fields = '__all__'
