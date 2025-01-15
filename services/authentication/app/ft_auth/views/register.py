########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import \
    HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import \
    require_http_methods

### Utils ###

from ft_auth.utils.user import \
    create_classic_user, check_user_register, \
    getLogin, getFirstName, getLastName
from ft_auth.utils.token import generate_jwt, get_jwt_data
from ft_auth.utils.single_page import single_page_redirection

@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
	data = get_jwt_data(request)
	if not "error" in data:
		return HttpResponseRedirect(f"/?{request.GET.urlencode()}")
	if request.method == "GET":
		return get_register(request)
	if request.method == "POST":
		return post_register(request)

def get_register(request):
	redirection = single_page_redirection(request)
	if redirection != None:
		return redirection
	return render(
			request,
			"/app/ft_auth/templates/register.html"
		)


def post_register(request):
	login = getLogin(request)
	first_name = getFirstName(request)
	last_name = getLastName(request)
	password = request.POST.get('password')

	error = check_user_register(
		login, first_name, last_name, password
    )
	if error is not None:
		context = {
			"error":
				error,
			"login": login,
			"first_name": first_name,
			"last_name": last_name
		}
		return render(
     		request,
            "/app/ft_auth/templates/register.html",
            context,
            status=401
        )
	user = create_classic_user(
		login, first_name, last_name, password
	)
	if user is None:
		return HttpResponse("Error")
	user_info = {
		"id": user.id,
		"role": "D"
	}
	response =  HttpResponseRedirect("/profil")
	generate_jwt(response, user_info)
	return response