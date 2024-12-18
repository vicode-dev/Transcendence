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

from os import environ
from ft_auth.utils.token import \
    get_jwt_data, generate_jwt
from ft_auth.utils.user import check_user_login
from ft_auth.utils.single_page import single_page_redirection
from ft_auth.utils.api_42 import get_context



@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request):
	data = get_jwt_data(request)
	if not "error" in data:
		return HttpResponseRedirect(f"/?{request.GET.urlencode()}")
	if request.method == "GET":
		return get_login(request)
	if request.method == "POST":
		return post_login(request)

def get_login(request):
	redirection = single_page_redirection(request)
	if redirection != None:
		return redirection
	return render(
		request,
		"/app/ft_auth/templates/login.html",
		get_context()
	)

def post_login(request):
	login = request.POST.get('login')
	password = request.POST.get('password')
	result = check_user_login(login, password)
	if "error" in result:
		return render(
			request,
			"/app/ft_auth/templates/login.html",	
			get_context(result),
			status=403
		)
	response = HttpResponseRedirect("/profil")
	generate_jwt(response, result["user"].to_dict())
	return response