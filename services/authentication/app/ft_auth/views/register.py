from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
	if request.method == "GET":
		return get_register(request)
	if request.method == "POST":
		return post_register()

def get_register(request):
	# return HttpResponseRedirect("https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-d994d34fee9548150795820d0569584f13de3c53f31275bffaf05b5860c6cf9f&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F42-oauth2&response_type=code");
	return render(request, "/app/app/templates/test.html")

def post_register():
	return HttpResponse("HTML TEST POST")