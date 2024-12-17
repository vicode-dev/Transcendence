from qrcode import make
from pyotp import totp
from io import BytesIO
from django.http import HttpResponse
from django import forms

class OTPForm(forms.Form):
    otp_code = forms.CharField(max_length=6, label="Code de vérification")

def generate_qr_code(user):

    otp_secret = user.otp_secret

    # Générer une URI conforme au protocole TOTP
    totp_uri = totp.TOTP(otp_secret).provisioning_uri(
        name=user.login,
        issuer_name="Transcendence"
    )

    # Générer le QR code
    qr = make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")