########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

### Utils ###

from ft_auth.utils.token import \
    get_jwt_data, generate_jwt
from ft_auth.utils.user import user_login
from ft_auth.utils.single_page import single_page_redirection

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
		"/app/ft_auth/templates/login.html"
	)

def post_login(request):
	login = request.POST.get('login')
	if login is None or len(login) == 0:
		context = {
			"error": _("You forgot to specify your login name.")
		}
		return render(
      			request,
         		"/app/ft_auth/templates/login.html",
				context
           )
	password = request.POST.get('password')
	if password is None or len(password) == 0:
		context = {
			"error": _("You forgot to specify your password."),
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
			"error": _("Login and password do not match."),
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