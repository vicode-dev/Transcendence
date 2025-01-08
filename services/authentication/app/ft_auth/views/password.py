########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

### Utils ###

from pyotp import TOTP
from ft_auth.utils.token import \
    get_jwt_data, generate_jwt
from ft_auth.utils.user import check_user_password, update_password, \
    get_user_by_id
from ft_auth.utils.single_page import single_page_redirection
from api.utils.otp_2fa import otp_is_required
from ft_auth.models import OTP

@csrf_exempt
@require_http_methods(["GET", "POST"])
def password(request):
	data = get_jwt_data(request)
	url = request.path
	query_params = request.GET.copy()
	query_params["redirect_url"] = url[1:]
	# return HttpResponse(data["error"])
	if "error" in data:
		return HttpResponseRedirect(f"/login/?{query_params.urlencode()}")
	if request.method == "GET":
		return get_password(request, data)
	if request.method == "POST":
		return post_password(request, data)

def get_password(request, data):
	redirection = single_page_redirection(request)
	if redirection != None:
		return redirection
	user = get_user_by_id(data["id"])
	return render(
		request,
		"/app/ft_auth/templates/password.html",
		context={
            "has_password": user.password is not None,
            "otp_required": otp_is_required(data["id"])
        }
	)

def post_password(request, data):
	oldpassword = request.POST.get('oldpassword')
	newpassword = request.POST.get('newpassword')
	code    	= request.POST.get('otp-code')
	result 		= check_user_password(data["id"], oldpassword, newpassword)
	if "error" in result:
		user = get_user_by_id(data["id"])
		return render(
			request,
			"/app/ft_auth/templates/password.html",	
			context={
                "error": result["error"],
                "has_password": user.password is not None,
                "otp_required": otp_is_required(data["id"])
            },
			status=401
		)
	otp = OTP.objects.filter(owner_id=result["user"].id).first()
	if otp is not None and otp.validated is True:
		totp = TOTP(otp.secret)
		if not totp.verify(code):
			user = get_user_by_id(data["id"])
			return render(
			request,
			"/app/ft_auth/templates/password.html",	
			context={
                "error": _("Invalid A2F code"),
                "has_password": user.password is not None,
                "otp_required": otp_is_required(data["id"])
            },
			status=401
		)
	response = render(request, "/app/ft_auth/templates/password_updated.html")
	update_password(result["user"], newpassword)
	generate_jwt(response, result["user"].to_dict())
	return response