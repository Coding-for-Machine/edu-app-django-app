from rest_framework import serializers

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, min_length=6)