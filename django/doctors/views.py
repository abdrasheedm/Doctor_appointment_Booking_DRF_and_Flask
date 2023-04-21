from django.shortcuts import render

# rest_framework import
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status


# Local imports
from .serializers import CategoryLIstSerializer, GetDoctorSerializer
from .models import Category, Doctors
# Create your views here.

class CategoryListView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryLIstSerializer


class GetDoctorsView(APIView):
    def get(self, request : Request):
        cat_id = request.query_params['_id']
        try:
            doctors = Doctors.objects.filter(category=cat_id)
            serializer = GetDoctorSerializer(instance=doctors, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        except:
            return Response({"message" : "Invalid Id"}, status=status.HTTP_404_NOT_FOUND)