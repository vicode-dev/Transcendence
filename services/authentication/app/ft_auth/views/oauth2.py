########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

### Utils ###

import requests
from ft_auth.utils.token import generate_jwt
from ft_auth.utils.api_42 import \
	get_42_user_access, get_42_user
from ft_auth.utils.user import \
	get_user_by_42_id, create_42_user

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
			user = create_42_user(user_42_data)
		if user is None:
			return JsonResponse({"error": _("User creation failed, try later.")}, status=500)
		response = HttpResponse(
			"<body onload=\"close();\"></body>"
		)
		if generate_jwt(response, user.to_dict()) is None:
			return JsonResponse({"error": _("User login failed, try later.")}, status=500)
		return response

	except requests.exceptions.RequestException as e:
		return JsonResponse({"error": _(str(e))}, status=500)