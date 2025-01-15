########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

### Utils ###

from pyotp import TOTP
from ft_auth.utils.token import \
    get_jwt_data, generate_jwt
from ft_auth.utils.single_page import single_page_redirection
from ft_auth.models import OTP, User

@csrf_exempt
@require_http_methods(["GET", "POST"])
def otp_page(request):
	data = get_jwt_data(request)
	# return JsonResponse(data)
	# if "error" not in data:
	# 	return HttpResponseRedirect(f"/?{request.GET.urlencode()}")
	# if data["error"] is not "OTP required":
	# 	return HttpResponseRedirect(f"/login/?{request.GET.urlencode()}")
	if request.method == "GET":
		return get_otp_page(request)
	if request.method == "POST":
		return post_otp(request, data)

def get_otp_page(request):
	redirection = single_page_redirection(request)
	if redirection != None:
		return redirection # 404
	return render(
		request,
		"/app/ft_auth/templates/otp.html"
	)

def post_otp(request, data):
	otp = OTP.objects.filter(owner_id=data["id"]).first()
	code = request.POST.get('otp-code')
	if code is None:
		return HttpResponse(False, status=400)
	totp = TOTP(otp.secret)
	if totp.verify(code):
		response = HttpResponse("")
		user = User.objects.filter(id=data["id"]).first()
		generate_jwt(response, user.to_dict())
		return response
	return render(
			request,
			"/app/ft_auth/templates/otp.html",
			status=401,
			context={
				"error":
        			_("Invalid code")
			}
		)