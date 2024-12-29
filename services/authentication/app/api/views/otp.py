########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponseRedirect, HttpResponse

### Utils ###

from pyotp import TOTP
from api.models import OTP
from api.utils.otp_2fa import generate_qr_code
from ft_auth.utils.token import get_jwt_data
from django.views.decorators.http import \
    require_http_methods
from ft_auth.utils.user import get_user_by_id

@require_http_methods(["GET"])
def request_qr_code(request):
	data = get_jwt_data(request)
	if data == None or "error" in data:
		return HttpResponseRedirect("/login")
	user = get_user_by_id(data["id"])
	return (generate_qr_code(user))

@require_http_methods(["GET"])
def check_otp_state(request):
	data = get_jwt_data(request)
	if data == None or "error" in data:
		return HttpResponse(False)
	otp = OTP.objects.filter(owner_id=data["id"]).first();
	if otp is None or otp.validated is False:
		return HttpResponse(False)
	return HttpResponse(True)

@require_http_methods(["POST"])
def validate_otp_code(request):
	data = get_jwt_data(request)
	if data == None or "error" in data:
		return HttpResponseRedirect("/login")
	otp = OTP.objects.filter(owner_id=data["id"]).first();
	if not otp:
		otp = OTP(owner_id=data["id"]);
		otp.save()
	code = request.POST.get('otp-code')
	if code is None:
		return HttpResponse(False, status=400)
	totp = TOTP(otp.secret)
	if totp.verify(code):
		otp.validated = True
		otp.save()
		return HttpResponse(True)
	return HttpResponse(False, status=401)

@require_http_methods(["GET"])
def disable_otp(request):
	data = get_jwt_data(request)
	if data == None or "error" in data:
		return HttpResponse(False)
	otp = OTP.objects.filter(owner_id=data["id"]).first();
	if otp is None or otp.validated is False:
		return HttpResponse(True)
	otp.delete()
	return HttpResponse(True)