import pyotp
from .models import Session

def generate_opt(user):
    session, _ = Session.objects.get_or_create(user=user)
    totp = pyotp.TOTP(session.secret)
    return totp.now() 


def verify_otp(user, code):
    try:
        session = Session.objects.get(user=user)
        totp = pyotp.TOTP(session.secret)
        return totp.verify(code, valid_window=1)  # 1 sikl farqni ham hisobga oladi (masalan, 30s kechikish)
    except Session.DoesNotExist as e:
        return False