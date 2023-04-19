# rest_framework
from rest_framework import serializers
from rest_framework.validators import ValidationError

# django imports
from django.core.validators import validate_email

# Local Imports
from .models import Account


# Signup serializer
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password')

    def validate(self, data):
        # email validation
        is_email_exist = Account.objects.filter(email = data['email']).exists()
        if is_email_exist:
            return ValidationError("This email is already taken")
        return super().validate(data)
    

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError("This is not a valid email address")

        return value
    
    
    # creating user
    def create(self, validated_data):
        # Hashing password
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user