from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ft_auth.utils.user import create_classic_user
from ft_auth.utils.token import generate_jwt

@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
	if request.method == "GET":
		return get_register(request)
	if request.method == "POST":
		return post_register(request)

def get_register(request):
	# return HttpResponseRedirect("https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-d994d34fee9548150795820d0569584f13de3c53f31275bffaf05b5860c6cf9f&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F42-oauth2&response_type=code");
	return render(request, "/app/ft_auth/templates/register.html")

def post_register(request):
    # if request.POST.get('login') is None:
    # if request.POST.get('first_name') is None:
    # if request.POST.get('last_name') is None:
    # if request.POST.get('password') is None:

	user = create_classic_user(
		request.POST.get('login'),
		request.POST.get('first_name'),
		request.POST.get('last_name'),
  		request.POST.get('password')
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