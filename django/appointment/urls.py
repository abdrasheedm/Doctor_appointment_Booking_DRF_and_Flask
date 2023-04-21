from django.urls import path, include
from .views import GetTimeSlotsView, BookSlotView, BookedAppointmentsView, DeleteSlotView


urlpatterns = [
    path('time-slots/', GetTimeSlotsView.as_view(), name="time_slots_view"),
    path('book-slot/', BookSlotView.as_view(), name="book_slot_view"),
    path('booked-appointments/', BookedAppointmentsView.as_view(), name="appointments"),
    path('delete-slot/', DeleteSlotView.as_view(), name="delete-slot"),
]