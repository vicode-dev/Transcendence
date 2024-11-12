from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
from ft_auth.utils.token import generate_jwt

from ft_auth.utils.api_42 import \
	get_42_user_access, get_42_user
from ft_auth.utils.user import \
	get_user_id_by_42_id, get_user_by_42_id, create_42_user

@csrf_exempt
@require_http_methods(["GET"])
def login_with_42(request):
	code = request.GET.get("code")
	if code is None:
		return (HttpResponseRedirect("/login"))

	try:
		user_access = get_42_user_access(code)
		
		user_42_data = get_42_user(user_access["access_token"])
		# print(user_access["access_token"])
		user = get_user_by_42_id(user_42_data["id"])
		if user == None:
			user = create_42_user(user_42_data)
		print(user.to_dict())
		response = HttpResponse(user)
		generate_jwt(response, user.to_dict())
		return response

	except requests.exceptions.RequestException as e:
		print("error", str(e))
		#return JsonResponse({"error": str(e)}, status=500)
		return HttpResponseRedirect("https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-d994d34fee9548150795820d0569584f13de3c53f31275bffaf05b5860c6cf9f&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F42-oauth2&response_type=code");
