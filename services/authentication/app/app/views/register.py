from django.http import HttpResponse
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
	return render(request, "/app/app/templates/test.html")

def post_register():
	return HttpResponse("HTML TEST POST")