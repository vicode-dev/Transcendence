########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ft_auth.utils.token import delete_jwt
from ft_auth.utils.user import delete_user, user_login


### Utils ###

from ft_auth.utils.user import \
	get_user_by_42_id, create_42_user, create_classic_user

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request):
	if request.method == "GET":
		return get_login(request)
	if request.method == "POST":
		return post_login(request)

def get_login(request):
	return render(request, "/app/ft_auth/templates/login.html")
	return JsonResponse(get_jwt_data(request))

def post_login(request):
	if request.POST.get('password') is None:
		return HttpResponse("I need your password");
	if request.POST.get('login') is None:
		return HttpResponse("I need your login");
	user = user_login(request.POST.get('login'), request.POST.get('password'))
	if user is None:
		return HttpResponse("invalid");
	return HttpResponseRedirect("/profil")

@require_http_methods(["GET"])
def logout(request):
	response = HttpResponseRedirect("/login")
	# delete_user("test")
	delete_jwt(response)
	return response