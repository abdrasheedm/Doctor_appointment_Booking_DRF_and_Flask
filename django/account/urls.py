from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('veriy-otp/', views.verify_otpView.as_view(), name = 'verify_otp'),
    path('signin/', views.LoginView.as_view(), name = 'signin'),
]
