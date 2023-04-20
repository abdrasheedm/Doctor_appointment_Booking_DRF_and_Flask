# Django imports
from django.shortcuts import render
from django.contrib.auth import authenticate

# Local imports
from .models import Account
from .serializer import SignUpSerializer
from .otp import send_otp, verify_otp
from .tokens import create_jwt_pair_tokens

#rest framework imports
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request : Request):
        email = request.data.get('email')
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # send_otp(request.data.get('phone_number'))
            response = {
                "message" : "User created Succesfully"
            }
            return Response(data = response, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            errorMessage = "Error occurred Please check your inputs"
            if Account.objects.filter(email=email).exists():
                errorMessage = "Email is already taken"
            if Account.objects.filter(phone_number=request.data.get('phone_number')).exists():
                errorMessage = "Phone number already Taken"
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)




class verify_otpView(APIView):

    def post(self, request : Request):
        data = request.data
        check_otp = data.get('otp')
        phone_number = data.get('phone_number')
        print(check_otp, phone_number)
        # check = verify_otp(phone_number, check_otp)
        check = True

        if check:
            user = Account.objects.get(phone_number = phone_number)
            user.is_verified = True
            user.save()

            return Response(data={'message': 'Account Verifed successfully'}, status=status.HTTP_200_OK)

        else:
            return Response(
                data={'message': 'Verification Failed. Please Check your otp'}, status=status.HTTP_400_BAD_REQUEST
            )
        

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request : Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password = password)

        if user is not None:
            if user.is_verified == True:
                tokens = create_jwt_pair_tokens(user)
                response = {
                    "message" : "Login Successful",
                    "token" : tokens,
                    "user_id" : user.id,
                }
                return Response(data=response, status=status.HTTP_200_OK)

            else:
                return Response({"message": "user is not verified"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message" : "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)