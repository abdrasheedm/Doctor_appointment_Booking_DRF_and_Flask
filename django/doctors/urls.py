from django.urls import path, include

# RestFramewrok import
from rest_framework import routers

from .views import CategoryListView, GetDoctorsView
from account.views import LoginView

router = routers.DefaultRouter()
router.register(r'categories', CategoryListView, basename = 'view-category')

urlpatterns = [
    path('', include(router.urls)),
    path('get-doctors-by-category/', GetDoctorsView.as_view(), name="get_doctor_by_category"),
]


