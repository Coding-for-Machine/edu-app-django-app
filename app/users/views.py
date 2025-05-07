from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Session
from .serializers import RegisterSerializer, OTPVerifySerializer
import pyotp

class AuthInitView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(
                {"detail": "Telefon raqam kiritilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user, created= User.objects.get_or_create(phone_number=phone_number)
            session, _ = Session.objects.get_or_create(user=user)
            
            # OTP generatsiya
            totp = pyotp.TOTP(session.secret)
            otp_code = totp.now()
            
            # Telefon raqamni sessionga saqlash
            request.session['auth_phone'] = phone_number
            request.session.set_expiry(300)  # 5 daqiqalik session
            
            # DEBUG: Productionda bu qism o'chiriladi yoki Telegram/SMS ga yuboriladi
            print(f"DEBUG: {phone_number} uchun OTP kodi: {otp_code}")
            
            return Response(
                {"message": "OTP kodi yuborildi"}, 
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {"detail": "Ushbu telefon raqam ro'yxatdan o'tmagan"},
                status=status.HTTP_404_NOT_FOUND
            )


class LoginView(APIView):
    def post(self, request):
        # Avval telefon raqam sessionda saqlanganligini tekshiramiz
        phone_number = request.session.get('auth_phone')
        if not phone_number:
            return Response(
                {"detail": "Telefon raqam topilmadi. Iltimos, avval telefon raqamingizni kiriting."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp']

            try:
                user = User.objects.get(phone_number=phone_number)
                session = Session.objects.get(user=user)

                totp = pyotp.TOTP(session.secret)
                if totp.verify(otp_code, valid_window=1):  # 30s derazada
                    # OTP to'g'ri bo'lsa, JWT tokenlarni yaratamiz
                    refresh = RefreshToken.for_user(user)
                    
                    # Sessionni tozalash
                    if 'auth_phone' in request.session:
                        del request.session['auth_phone']
                    
                    return Response({
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    })
                else:
                    return Response(
                        {"detail": "OTP noto'g'ri yoki eskirgan"}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                return Response(
                    {"detail": "Foydalanuvchi topilmadi"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Session.DoesNotExist:
                return Response(
                    {"detail": "OTP sessiyasi topilmadi"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)