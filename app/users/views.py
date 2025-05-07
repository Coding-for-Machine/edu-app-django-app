from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Session
from .serializers import PhoneNumberSerializer, OTPVerifySerializer
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
            # Foydalanuvchi yaratish yoki olish
            user, created = User.objects.get_or_create(phone_number=phone_number)
            
            # Session yaratish
            session, _ = Session.objects.get_or_create(user=user)
            
            # OTP generatsiya
            totp = pyotp.TOTP(session.secret, interval=60)
            otp_code = totp.now()
            
            # Sessionga telefon raqamni saqlash
            request.session['auth_phone'] = phone_number
            request.session['otp_secret'] = session.secret  # Secretni ham saqlab qo'yamiz
            request.session.save()  # Sessionni saqlashni unutmang!
            
            print(f"Session ID: {request.session.session_key}")
            print(f"Session data: {request.session.items()}")
            
            return Response(
                {"message": "OTP kodi yuborildi", "code": otp_code},  # Faqat test uchun
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"detail": f"Xatolik yuz berdi: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
class LoginView(APIView):
    def post(self, request):
        # Sessiondan ma'lumotlarni olish
        phone_number = request.session.get('auth_phone')
        otp_secret = request.session.get('otp_secret')
        
        print(f"LoginView session data - Phone: {phone_number}, Secret: {otp_secret}")
        
        if not phone_number or not otp_secret:
            return Response(
                {"detail": "Telefon raqam topilmadi. Iltimos, avval OTP so'rovini yuboring."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        otp_code = serializer.validated_data['otp']

        try:
            # OTP ni tekshirish
            totp = pyotp.TOTP(otp_secret)
            current_otp = totp.now()
            
            print(f"OTP tekshirish - Server: {current_otp}, Kelgan: {otp_code}")
            
            if not totp.verify(otp_code, valid_window=1):
                return Response(
                    {"detail": "OTP noto'g'ri yoki eskirgan"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Foydalanuvchini olish
            user = User.objects.get(phone_number=phone_number)
            
            # Token yaratish
            refresh = RefreshToken.for_user(user)
            
            # Sessionni tozalash
            request.session.flush()
            
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        except User.DoesNotExist:
            return Response(
                {"detail": "Foydalanuvchi topilmadi"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"Xatolik yuz berdi: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetSessionView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response(
                {"detail": "Telefon raqam kiritilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(phone_number=phone_number)
            session = Session.objects.get(user=user)
            return Response({"session_id": session.id})
        except (User.DoesNotExist, Session.DoesNotExist):
            return Response(
                {"detail": "Session topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )