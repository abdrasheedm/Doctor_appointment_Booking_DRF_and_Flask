from django.shortcuts import render

#rest_framework imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

# local imports
from .serializers import TimeSlotSerializer, BookSlotSerializer, BookedAppointmentSerializer
from .models import Appointment, AppointmentBook
# Create your views here.


class GetTimeSlotsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request:Request):
        doc_id = request.query_params['doc_id']
        try:
            slots = Appointment.objects.filter(doctor=doc_id, is_available=True)
            serializer = TimeSlotSerializer(instance=slots, many = True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except:
            return Response({"message" : "Invalid input"}, status=status.HTTP_404_NOT_FOUND)
        

class BookSlotView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request : Request):
        print(request.data, '---------------------------------')
        serializer = BookSlotSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Slot booked successfully"}, status=status.HTTP_201_CREATED)
        
        else:
            print(serializer.errors)
            return Response({"message" : "Invalid inputs"}, status=status.HTTP_400_BAD_REQUEST)
        

    
class BookedAppointmentsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request:Request):
        u_id = request.query_params['user_id']
        try:
            slots = AppointmentBook.objects.filter(user=u_id)
            serializer = BookedAppointmentSerializer(instance=slots, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except:
            return Response({"message" : "Invalid creadentials"}, status=status.HTTP_400_BAD_REQUEST)
        


class DeleteSlotView(APIView):

    permission_classes = [IsAuthenticated]
    
    def delete(self, request:Request):
        slot_id = request.query_params['slot_id']
        try:
            instance = AppointmentBook.objects.get(id = slot_id)
            instance.appointment.is_available = True
            instance.appointment.save()
            instance.delete()
            return Response({"message": "Slot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except:
            return Response({"message": "Invalid Id"}, status=status.HTTP_404_NOT_FOUND)