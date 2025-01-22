########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

### Utils ###

from pyotp import TOTP
from ft_auth.utils.token import \
    get_jwt_data, get_link_jwt_data
from ft_auth.utils.user import check_user_password, \
    get_user_by_id
from ft_auth.utils.single_page import single_page_redirection
from api.utils.otp_2fa import otp_is_required
from ft_auth.models import OTP
from ft_auth.utils.api_42 import get_42_url
from ft_auth.utils.user import get_user_by_login, \
    get_user_by_id

@csrf_exempt
@require_http_methods(["GET", "POST"])
def link(request):
	data = get_jwt_data(request)
	link_data = get_link_jwt_data(request)
	url = request.path
	query_params = request.GET.copy()
	query_params["redirect_url"] = url[1:]
	if "error" in link_data:
		redirection = single_page_redirection(request)
		if redirection is not None:
			return redirection
		return render(request,
            "/app/ft_auth/templates/to_42.html",
            context={
			"domain_name": get_42_url()
		})
	if "error" in data:
		user = get_user_by_login(link_data["login"])
		data = user.to_dict()
		# return HttpResponseRedirect(f"/login/?{query_params.urlencode()}")
	if request.method == "GET":
		return get_link(request, data, link_data)
	if request.method == "POST":
		return post_link(request, data, link_data)

def get_link(request, data, link_data):
	redirection = single_page_redirection(request)
	if redirection is not None:
		return redirection
	user = get_user_by_id(data["id"])
	return render(
		request,
		"/app/ft_auth/templates/link.html",
		context={
            "has_password": user.password is not None,
            "otp_required": otp_is_required(data["id"]),
            "login": user.login
        }
	)

def post_link(request, data, link_data):
	password	= request.POST.get('password')
	code    	= request.POST.get('otp-code')
	result 		= check_user_password(data["id"], password)
	user		= get_user_by_id(data["id"])
	if "error" in result:
		return render(
			request,
			"/app/ft_auth/templates/link.html",	
			context={
                "error": result["error"],
                "has_password": user.password is not None,
                "otp_required": otp_is_required(data["id"]),
                "login": user.login
            },
			status=401
		)
	otp = OTP.objects.filter(owner_id=result["user"].id).first()
	if otp is not None and otp.validated is True:
		totp = TOTP(otp.secret)
		if not totp.verify(code):
			return render(
			request,
			"/app/ft_auth/templates/link.html",	
			context={
                "error": _("Invalid A2F code"),
                "has_password": user.password is not None,
                "otp_required": otp_is_required(data["id"]),
                "login": user.login
            },
			status=401
		)
	response = render(request, "/app/ft_auth/templates/linked.html")
	user.ft_id = link_data["ft_id"]
	user.save()
	response.delete_cookie("update")
	response.delete_cookie("link")
	return response