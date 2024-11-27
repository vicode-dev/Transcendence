########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

### Utils ###

from ft_auth.utils.token import \
    delete_jwt, get_jwt_data, generate_jwt
from ft_auth.utils.user import user_login

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request):
	if request.method == "GET":
		return get_login(request)
	if request.method == "POST":
		return post_login(request)

def get_login(request):
	data = get_jwt_data(request)
	if "error" in data:
		return render(request, "/app/ft_auth/templates/login.html")
	return HttpResponseRedirect(f"/?{request.GET.urlencode()}")
	# return JsonResponse(get_jwt_data(request))

def post_login(request):
	login = request.POST.get('login')
	if login is None or len(login) == 0:
		context = {
			"error": "You forgot to specify your login name."
		}
		return render(
      			request,
         		"/app/ft_auth/templates/login.html",
				context
           )
	password = request.POST.get('password')
	if password is None or len(password) == 0:
		context = {
			"error": "You forgot to specify your password.",
			"login": login
		}
		return render(
      			request,
         		"/app/ft_auth/templates/login.html",
				context
           )

	user = user_login(login, password)
	if user is None:
		context = {
			"error": "Login and password do not match.",
			"login": login
		}
		return render(
      			request,
         		"/app/ft_auth/templates/login.html",
				context
           )
	response = HttpResponseRedirect("/profil")
	generate_jwt(response, user.to_dict())
	return response

@require_http_methods(["GET"])
def logout(request):
	response = HttpResponseRedirect("/login")
	# delete_user("test")
	delete_jwt(response)
	return response