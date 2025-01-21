########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponseRedirect, \
    JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

### Utils ###

import requests
from ft_auth.utils.token import generate_jwt, generate_link_jwt
from ft_auth.utils.api_42 import \
	get_42_user_access, get_42_user
from ft_auth.utils.user import get_user_by_login,\
	get_user_by_42_id, create_42_user
from api.utils.otp_2fa import otp_is_required

@csrf_exempt
@require_http_methods(["GET"])
def login_with_42(request):
	code = request.GET.get("code")
	if code is None:
		return (HttpResponseRedirect("/login"))
	try:
		user_access = get_42_user_access(code)
		user_42_data = get_42_user(user_access["access_token"])
		user = get_user_by_42_id(user_42_data["id"])
		if user is None:
			user = get_user_by_login(user_42_data["login"])
			if user is None:
				user = create_42_user(user_42_data)
			else:
				response = HttpResponse(
					"<body onload=\"close();\"></body>"
				)
				generate_link_jwt(response, user_42_data)
				return response
				return render(request,
					"/app/ft_auth/templates/link.html",
					context={
						"has_password": user.password is not None,
						"otp_required": otp_is_required(user.id)
					})
		if user is None:
			return JsonResponse({"error": _("User creation failed, try later.")}, status=500)
		response = HttpResponse(
			"<body onload=\"close();\"></body>"
		)
		otp_required = otp_is_required(user.id)
		if generate_jwt(response, user.to_dict(), otp_required, login_with_42=True) is None:
			return JsonResponse({"error": _("User login failed, try later.")}, status=500)
		return response

	except requests.exceptions.RequestException as e:
		return JsonResponse({"error": _(str(e))}, status=500)