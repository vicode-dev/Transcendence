########################################################
###                Dependencies                      ###
########################################################

### Django ###

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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
	test = f"{request.POST.get('user_name')}:{request.POST.get('user_password')}"
 
	return HttpResponse(test);