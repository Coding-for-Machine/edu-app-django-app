from rest_framework import serializers
from .models import User, Session
import pyotp

class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)

    def create(self, validated_data):
        user, created = User.objects.get_or_create(phone_number=validated_data['phone_number'])
        Session.objects.get_or_create(user=user)
        return user


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
