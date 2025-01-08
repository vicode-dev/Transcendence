from qrcode import make
from pyotp import totp
from io import BytesIO
from django.http import HttpResponse
from django import forms

from api.models import OTP

class OTPForm(forms.Form):
    otp_code = forms.CharField(max_length=6, label="Code de vérification")

def generate_qr_code(user):
    otp = OTP.objects.filter(owner_id=user.id).first()
    if otp is None:
        otp = OTP(owner_id=user.id)
        otp.save()

    # Générer une URI conforme au protocole TOTP
    totp_uri = totp.TOTP(otp.secret).provisioning_uri(
        name=user.login,
        issuer_name="Transcendence"
    )

    # Générer le QR code
    qr = make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")

def otp_is_required(user_id):
	otp = OTP.objects.filter(owner_id=user_id).first();
	if otp is None or otp.validated is False:
		return False
	return True