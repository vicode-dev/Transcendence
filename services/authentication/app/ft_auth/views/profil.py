from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from ft_auth.utils.token import get_jwt_data
from ft_auth.utils.user import get_user_by_id
from ft_auth.utils.api_users import get_user

@csrf_exempt
@require_http_methods(["GET"])
def profil(request):
	data = get_jwt_data(request)
	if data == None or "error" in data:
		return HttpResponseRedirect("/login")
	user = get_user_by_id(data["id"])
	if user == None:
		return HttpResponseForbidden()
	context = {
		"user_name": f"{user.first_name} {user.last_name}",
		"role" : get_user(user.id, target="role")["role"]
	}
	
	return render(request, "/app/ft_auth/templates/profil.html", context)

